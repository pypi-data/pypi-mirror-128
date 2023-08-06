"""
ISO 14229 UDS protocol
"""
import struct
from enum import IntEnum
from queue import Queue, Empty
from threading import Thread
from typing import Optional

import socketcan as socketcan


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


class Uds:
    """
    UDS Protocol class

    depends on socketcan
    therefore runs on linux only
    """

    def __init__(self,
                 socket: socketcan.CanIsoTpSocket
                 ):
        """
        Constructor

        :param socket: A SocketCAN IsoTp socket.
        """
        self._s = socket
        self.timeout = 5  # 5 seconds
        self.rx_queue = Queue()
        self.rx_handler = Thread(target=self._handle_rx)
        self.rx_handler.setDaemon(True)
        self.rx_handler.start()

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
        It may raise a TimeoutError if rx_queue was empty.
        :return: Data bytes.
        :raises TimeoutError
        """
        try:
            data = self.rx_queue.get(timeout=self.timeout)
        except Empty:
            raise TimeoutError
        else:
            return data

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
        self._send(req)
        return self._recv()
