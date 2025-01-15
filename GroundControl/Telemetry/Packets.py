from enum import Enum
import struct


class PacketType(Enum):
    DEFAULT = 0
    MOTION = 1
    CAMERA_ROTATION = 2
    UNUSED = 3
    THROTTLE = 4


class PacketProtocol:
    def __init__(self, packetType=PacketType.DEFAULT, decoded=''):
        self.header_format = "I I"

        self.header = {
            'packetType': packetType,
            'decodedLen': 0
        }
        self.decoded = decoded
        self.crc16 = 0

        if isinstance(self.decoded, str):
            self.decoded = self.decoded.encode()  # not our encode, str encode to bytes

        self.packet = ''

    def encode(self):
        self.header['decodedLen'] = len(self.decoded)

        header = struct.pack(self.header_format, self.header['packetType'].value, self.header['decodedLen'])
        self.crc16 = self.calculateCRC16(header + self.decoded)
        # footer = struct.pack(self.footer_format, self.crc16)

        self.packet = header + self.decoded + self.crc16
        return self.packet

    def decode(self, encoded):
        headerSize = struct.calcsize(self.header_format)
        footerSize = struct.calcsize("!H")

        self.crc16 = encoded[len(encoded) - footerSize - 1:len(encoded) - 1]
        newCRC16 = self.calculateCRC16(encoded[:len(encoded) - footerSize - 1])

        if self.crc16 == newCRC16:
            header = encoded[:headerSize]

            self.header['packetType'] = struct.unpack(self.header_format, header)[0]
            self.header['decodedLen'] = struct.unpack(self.header_format, header)[1]
            self.decoded = encoded[headerSize:headerSize + self.header['decodedLen']].decode()
            return True

        # print('UNPACKETIZE CHECKSUM ERROR -- DROPPING PACKET')
        return False

    def getDecoded(self):
        return self.decoded

    def getEncoded(self):
        return self.packet

    def getPacketType(self):
        return self.header['packetType']

    def calculateCRC16(self, decoded):
        crc = 0xFFFF
        for byte in decoded:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, byteorder='little')

