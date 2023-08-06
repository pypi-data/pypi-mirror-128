"""
ISO 14229 UDS protocol
"""
import datetime
import struct
from enum import IntEnum
from queue import Queue, Empty
from threading import Thread
from typing import Optional

import socketcan as socketcan

import logging

LOGGER = logging.getLogger(__name__)


class DiagnosticSessions(IntEnum):
    DefaultSession = 1
    ProgrammingSession = 2
    ExtendedDiagnosticSession = 3
    SafetySystemDiagnosticSession = 4


class ServiceIds(IntEnum):
    # Diagnostic and Communication Management
    DiagnosticSessionControl = 0x10
    EcuReset = 0x11
    SecurityAccess = 0x27
    CommunicationControl = 0x28
    TesterPresent = 0x3E
    AccessTimingParameter = 0x83
    SecuredDataTransmission = 0x84
    ControlDtcSettings = 0x85
    ResponseOnEvent = 0x86
    LinkControl = 0x87

    # Data Transmission
    ReadDataByIdentifier = 0x22
    ReadMemoryByAddress = 0x23
    ReadScalingDataByIdentifier = 0x24
    ReadDataByPeriodicIdentifier = 0x2A
    DynamicallyDefineDataIdentifier = 0x2C
    WriteDataByIdentifier = 0x2E
    WriteMemoryByAddress = 0x3D

    # Stored Data Transmission
    ClearDiagnosticInformation = 0x14
    ReadDtcInformation = 0x19

    # Input / Output Control
    InputOutputByIdentifier = 0x2F

    # Remote Activation of Routine
    RoutineControl = 0x31

    # Upload / Download
    RequestDownload = 0x34
    RequestUpload = 0x35
    DataTransfer = 0x36
    RequestTransferExit = 0x37


class ResponseCodes(IntEnum):
    """
    UDS Negative Response Codes

    Some Explanation, when ISO14229 (UDS) was made,
    it had to be compatible with the preceding ISO14230 (KWP2000)
    so everything up to the 0x40 range is nearly identical.
    BTW: See how BOSCH managed to fake the ISO numbering.
    There are some unofficial ranges for different topics
    0x10-0x1F, 0x20-0x2F and so on.
    """
    # tester side error
    GeneralReject = 0x10
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12
    IncorrectMessageLengthOrInvalidFormat = 0x13
    ResponseTooLong = 0x14

    # device side error
    BusyRepeatRequest = 0x21
    ConditionsNotCorrect = 0x22
    RequestSequenceError = 0x24
    NoResponseFromSubnetComponent = 0x25
    FaultPreventsExecutionOfRequestedAction = 0x26

    # function side error
    RequestOutOfRange = 0x31
    SecurityAccessDenied = 0x33
    InvalidKey = 0x35
    ExceededNumberOfAttempts = 0x36
    RequiredTimeDelayNotExpired = 0x37

    # 0x38-0x4F Reserved by Extended Data Link Security Document

    UploadDownloadNotAccepted = 0x70
    TransferDataSuspended = 0x71
    GeneralProgrammingFailure = 0x72
    WrongBlockSequenceCounter = 0x73

    RequestCorrectlyReceivedButResponsePending = 0x78
    # This is essentially not an Error, it is just a delay information.
    # This Response Code is due to the fact that standard autosar modules do not necessarily run on the same time disc
    # and no IPC method has every been defined for Autosar.

    SubFunctionNotSupportedInActiveSession = 0x7E
    ServiceNotSupportedInActiveSession = 0x7F


def parse_diagnostic_session_control_response(data: bytes) -> dict:
    """ parse function for specific response """
    return dict(zip(["P2_Server_Max", "P2*_Server_Max"], struct.unpack(">HH", data[2:])))


class Uds:
    """
    UDS Protocol class

    depends on socketcan
    therefore runs on linux only
    """

    def __init__(self,
                 socket: socketcan.CanIsoTpSocket,
                 timeout: int = 5,
                 ):
        """
        Constructor

        :param socket: A SocketCAN IsoTp socket.
        """
        self._s = socket
        self.timeout = timeout
        self.rx_queue = Queue()
        self.rx_handler = Thread(target=self._handle_rx)
        self.rx_handler.setDaemon(True)
        self.rx_handler.start()

    # basic functionality

    def _handle_rx(self) -> None:
        """
        Puts data from socket into a queue,
        where the requester (main thread) in self.recv()
        :return: Nothing.
        """
        while True:
            self.rx_queue.put(self._s.recv())

    def _send(self, data: bytes) -> int:
        """
        Sends data to the socket.
        :param data: The data to be sent.
        :return: The length of data that was sent.
        """
        return self._s.send(data=data)

    def _recv(self) -> Optional[bytes]:
        """
        Receives data from rx_queue in case it was filled by
        rx_handler.
        The underlying queue mechanism may raise an Empty Exception.
        :return: Data bytes.
        """
        return self.rx_queue.get(timeout=self.timeout)

    def request(self, req: bytes) -> Optional[bytes]:
        """
        Service request function
        It handles transmission, reception and check if a negative response error should be raised
        :param req: The request as bytes.
        :return: The response as bytes.
        :raises: Subtypes of NegativeResponse, UdsTimeoutError, etc.
        """
        bytes_sent = self._send(req)
        ts_request_sent = datetime.datetime.now()
        if bytes_sent != len(req):
            LOGGER.error("bytes_sent != len(data)")
        try:
            resp = self._recv()
        except Empty:
            raise UdsTimeoutError
        else:
            time_for_response = datetime.datetime.now() - ts_request_sent
            LOGGER.debug("Response received after timedelta {0}".format(time_for_response))
            is_positive_response = (resp[0] == (req[0] | 0x40))
            if not is_positive_response:
                response_code = ResponseCodes(resp[0])
                LOGGER.error("Request {0} returned {1}".format(req.hex(), response_code.name))
                raise RESPONSECODE_TO_EXCEPTION_MAPPING.get(response_code)
            else:
                return resp

    # convenience functions for specific services

    def diagnostic_session_control(self,
                                   session: DiagnosticSessions = DiagnosticSessions.ExtendedDiagnosticSession):
        """
        Basic uds service diagnostic session control.
        :param session: The requested diagnostic session.
        :return: The data that was returned.
        """
        assert session in DiagnosticSessions

        req = struct.pack("BB", ServiceIds.ReadDataByIdentifier, session)
        return self.request(req=req)

    def read_data_by_id(self,
                        did: int) -> Optional[bytes]:
        """
        Basic uds service read data by id.
        :param did: The diagnostic identifier to be read.
        :return: The data that was returned.
        :raises TimeoutError
        """
        if did not in range(0x10000):
            raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
        req = struct.pack(">BH", ServiceIds.ReadDataByIdentifier, did)
        return self.request(req=req)


# Exceptions

class UdsProtocolException(Exception):
    pass


class UdsTimeoutError(UdsProtocolException):
    pass


class NegativeResponse(UdsProtocolException):
    pass


class GeneralReject(NegativeResponse):
    pass


class ServiceNotSupported(NegativeResponse):
    pass


class SubfunctionNotSupported(NegativeResponse):
    pass


class IncorrectMessageLengthOrInvalidFormat(NegativeResponse):
    pass


class ResponseTooLong(NegativeResponse):
    pass


class BusyRepeatRequest(NegativeResponse):
    pass


class ConditionsNotCorrect(NegativeResponse):
    pass


class RequestSequenceError(NegativeResponse):
    pass


class NoResponseFromSubnetComponent(NegativeResponse):
    pass


class FaultPreventsExecutionOfRequestedAction(NegativeResponse):
    pass


class RequestOutOfRange(NegativeResponse):
    pass


class SecurityAccessDenied(NegativeResponse):
    pass


class InvalidKey(NegativeResponse):
    pass


class ExceededNumberOfAttempts(NegativeResponse):
    pass


class RequiredTimeDelayNotExpired(NegativeResponse):
    pass


class UploadDownloadNotAccepted(NegativeResponse):
    pass


class TransferDataSuspended(NegativeResponse):
    pass


class GeneralProgrammingFailure(NegativeResponse):
    pass


class WrongBlockSequenceCounter(NegativeResponse):
    pass


class RequestCorrectlyReceivedButResponsePending(NegativeResponse):
    # This is actually not a Negative Response, see how we can handle this in program flow,
    # maybe base on Exception instead.
    pass


class SubFunctionNotSupportedInActiveSession(NegativeResponse):
    pass


class ServiceNotSupportedInActiveSession(NegativeResponse):
    pass


RESPONSECODE_TO_EXCEPTION_MAPPING = {
    ResponseCodes.GeneralReject: GeneralReject,
    ResponseCodes.ServiceNotSupported: ServiceNotSupported,
    ResponseCodes.SubFunctionNotSupported: SubfunctionNotSupported,
    ResponseCodes.IncorrectMessageLengthOrInvalidFormat: IncorrectMessageLengthOrInvalidFormat,
    ResponseCodes.ResponseTooLong: ResponseTooLong,
    ResponseCodes.BusyRepeatRequest: BusyRepeatRequest,
    ResponseCodes.ConditionsNotCorrect: ConditionsNotCorrect,
    ResponseCodes.RequestSequenceError: RequestSequenceError,
    ResponseCodes.NoResponseFromSubnetComponent: NoResponseFromSubnetComponent,
    ResponseCodes.FaultPreventsExecutionOfRequestedAction: FaultPreventsExecutionOfRequestedAction,
    ResponseCodes.RequestOutOfRange: RequestOutOfRange,
    ResponseCodes.SecurityAccessDenied: SecurityAccessDenied,
    ResponseCodes.InvalidKey: InvalidKey,
    ResponseCodes.ExceededNumberOfAttempts: ExceededNumberOfAttempts,
    ResponseCodes.RequiredTimeDelayNotExpired: RequiredTimeDelayNotExpired,
    ResponseCodes.UploadDownloadNotAccepted: UploadDownloadNotAccepted,
    ResponseCodes.TransferDataSuspended: TransferDataSuspended,
    ResponseCodes.GeneralProgrammingFailure: GeneralProgrammingFailure,
    ResponseCodes.WrongBlockSequenceCounter: WrongBlockSequenceCounter,
    ResponseCodes.RequestCorrectlyReceivedButResponsePending: RequestCorrectlyReceivedButResponsePending,
    ResponseCodes.SubFunctionNotSupportedInActiveSession: SubFunctionNotSupportedInActiveSession,
    ResponseCodes.ServiceNotSupportedInActiveSession: ServiceNotSupportedInActiveSession,
}
