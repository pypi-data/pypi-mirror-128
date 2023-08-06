"""
Module containing handlers for Zabbix protocol.
"""

from typing import Optional, Dict
import abc
import socket
import struct
import logging
import json
from enum import Flag

logger = logging.getLogger(__name__)


class ProtocolFlags(Flag):
    ZABBIX = b'\x01'
    COMPRESSION = b"\x02"
    LARGE_PACKET = b"\x04"


class _Dstream(abc.ABC):
    def __init__(self, target: str, port: int = 10051, source_address: Optional[str] = None) -> None:
        self._ip = target
        self._port = port
        self._source_address = source_address

    def _send(self, payload: bytes) -> str:
        data = b""
        parsed = ""
        s = None
        try:
            if self._source_address:
                s = socket.create_connection(
                    (self._ip, self._port),
                    source_address=(self._source_address, 0))
                logger.info(f"Opening connection to {self._ip}:{self._port} with source address {self._source_address}")
            else:
                s = socket.create_connection((self._ip, self._port))
                logger.info(f"Opening connection to {self._ip}:{self._port}")
            packed = self._pack_request(payload)
            s.sendall(packed)
            data = self._recv_response(s)
            parsed = self._unpack_response(data)
        except socket.error:
            logger.exception(f"Cannot connect to host {self._ip}:{self._port}:")
        except struct.error:
            logger.exception("Recived response is corrupted:")
        except Exception:
            logger.exception("Something really bad happened:")
        finally:
            if s:
                logger.info(f"Closing connection to {self._ip}:{self._port}")
                s.close()
            return parsed

    def _unpack_response(self, response: bytes) -> str:
        HEADER_LEN = 13
        _, protocol, length, _ = struct.unpack('<4s1sLL', response[:HEADER_LEN])
        data = struct.unpack(
            f'<{length}s',
            response[HEADER_LEN:HEADER_LEN+length]
            )[0]

        return data.decode('utf-8')

    def _pack_request(self, payload: bytes) -> bytes:
        payload_len = len(payload)
        packed = struct.pack(
            f'<4scL4s{payload_len}s',
            b'ZBXD',
            ProtocolFlags.ZABBIX.value,
            payload_len,
            b"\x00\x00\x00\x00",
            payload
            )
        logger.debug(f"Packed payload for {self._ip}:{self._port}. Payload length: {payload_len}. Length with headers: {len(packed)}")
        return packed

    def _recv_response(self, socket_: socket.socket, buff: int = 1024) -> bytes:
        data = b""
        buffer = socket_.recv(buff)
        logger.debug(f"Received {len(buffer)} from {self._ip}:{self._port}")
        while buffer:
            data += buffer
            buffer = socket_.recv(buff)
            logger.debug(f"Received {len(buffer)} from {self._ip}:{self._port}")
        logger.debug(f"Completed data retrieval from {self._ip}:{self._port}. Total length: {len(data)}")
        return data

    @staticmethod
    def _parse_server_response(info) -> Optional[Dict]:
        try:
            response = json.loads(info)
        except json.decoder.JSONDecodeError:
            return None
        data = response.get('info', None)
        splitted = [x.strip().split(':') for x in data.split(';')]
        for i, split in enumerate(splitted):
            name, val = split
            splitted[i][1] = float(val) if name == 'seconds spent' else int(val)
        return dict(splitted)
