import threading
from time import sleep
from ServoController import ServoController
from Telemetry.PlaneTranceiver import PlaneTranceiver
from Telemetry.Packets import PacketProtocol, PacketType


class CommunicationHandler:

    def __init__(self, servoController):
        self.servoController = servoController

        self.planeTranceiver = PlaneTranceiver()
        self.planeReceiver = threading.Thread(target=self.planeTranceiver.receive)
        self.planeTransmitter = threading.Thread(target=self.planeTranceiver.transmit)
        self.planeReceiver.daemon = True
        self.planeTransmitter.daemon = False
        self.planeReceiver.start()
        self.planeTransmitter.start()

        self.processThread = threading.Thread(target=self.listen)
        self.processThread.daemon = True
        self.processThread.start()

    def listen(self):
        packet = PacketProtocol()

        while True:
            data = self.planeTranceiver.pull()
            if data is not None and packet.decode(data):
                if packet.getPacketType() == PacketType.MOTION.value:
                    motion = packet.getDecoded()
                    # print("Motion Packet Received: " + str(motion))
                    d_pitch, d_yaw, d_roll = list(map(float, motion.split(",")))
                    self.servoController.apply_motion_packet(d_pitch, d_yaw, d_roll)
                if packet.getPacketType() == PacketType.CAMERA_ROTATION.value:
                    rotation = packet.getDecoded()
                    # print("Camera Rotation Packet Received: " + str(rotation))
                    d_pitch, d_yaw = list(map(float, rotation.split(",")))
                    self.servoController.apply_camera_rotation_packet(d_pitch, d_yaw)
                if packet.getPacketType() == PacketType.THROTTLE.value:
                    d_throttle = packet.getDecoded()
                    # print("Throttle Packet Received: " + str(d_throttle))
                    self.servoController.apply_throttle_packet(float(d_throttle))

            sleep(0.01)

    def send_image(self, bytes):
        packet = PacketProtocol(packetType=PacketType.CAMERA_IMAGE, decoded=bytes)
        self.planeTranceiver.push(packet.encode(), 0)

