import threading
from time import sleep
import numpy as np
import cv2
from Telemetry.GroundTranceiver import GroundTranceiver
from Telemetry.Packets import PacketProtocol, PacketType


class CommunicationHandler:

    def __init__(self):
        self.groundTranceiver = GroundTranceiver()
        self.groundReceiver = threading.Thread(target=self.groundTranceiver.receive)
        self.groundTransmitter = threading.Thread(target=self.groundTranceiver.transmit)
        self.groundReceiver.daemon = True
        self.groundTransmitter.daemon = False
        self.groundReceiver.start()
        self.groundTransmitter.start()

        self.processThread = threading.Thread(target=self.listen)
        self.processThread.daemon = True
        self.processThread.start()

        self.frame = np.zeros((1280, 720, 3), dtype=np.uint8)

    def listen(self):
        packet = PacketProtocol()

        while True:
            data = self.groundTranceiver.pull()
            if data is not None and packet.decode(data):
                print("received")
                if packet.getPacketType() == PacketType.MOTION.value:
                    print("Motion")
                    motion = packet.getDecoded()
                if packet.getPacketType() == PacketType.CAMERA_IMAGE.value:
                    bytes = packet.getDecoded()
                    np_arr = np.frombuffer(bytes, np.uint8)
                    self.frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            sleep(0.01)

    def send_motion(self, d_pitch, d_yaw, d_roll):
        packet = PacketProtocol(packetType=PacketType.MOTION, decoded=f"{d_pitch},{d_yaw},{d_roll}")
        self.groundTranceiver.push(packet.encode(), 0)

    def send_camera_rotation(self, d_pitch, d_yaw):
        packet = PacketProtocol(packetType=PacketType.CAMERA_ROTATION, decoded=f"{d_pitch},{d_yaw}")
        self.groundTranceiver.push(packet.encode(), 0)

    def send_throttle(self, d_throttle):
        packet = PacketProtocol(packetType=PacketType.MOTION, decoded=f"{d_throttle}")
        self.groundTranceiver.push(packet.encode(), 0)



