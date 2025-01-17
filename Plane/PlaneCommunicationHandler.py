import threading
from time import sleep
from ServoController import ServoController
from Telemetry.Tranceiver import Tranceiver
from Telemetry.Packets import PacketProtocol, PacketType


class CommunicationHandler:

    def __init__(self, servoController):
        self.servoController = servoController

        self.planeTranceiver = Tranceiver()
        self.planeReceiver = threading.Thread(target=self.planeTranceiver.receive)
        self.planeTransmitter = threading.Thread(target=self.planeTranceiver.transmit)
        self.planeReceiver.daemon = True
        self.planeTransmitter.daemon = False
        self.planeReceiver.start()
        self.planeTransmitter.start()

        self.processThread = threading.Thread(target=self.listen)
        self.processThread.daemon = True
        self.processThread.start()
        print("PlaneCommunicationHandler Thread Started!")

    def listen(self):
        packet = PacketProtocol()

        while True:
            data = self.planeTranceiver.pull()
            if data is not None and packet.decode(data):
                if packet.getPacketType() == PacketType.MOTION.value:
                    motion = packet.getDecoded()
                    d_pitch, d_yaw, d_roll = list(map(float, motion.split(",")))
                    self.servoController.apply_motion_packet(d_pitch, d_yaw, d_roll)
                if packet.getPacketType() == PacketType.CAMERA_ROTATION.value:
                    rotation = packet.getDecoded()
                    d_pitch, d_yaw = list(map(float, rotation.split(",")))
                    self.servoController.apply_camera_rotation_packet(d_pitch, d_yaw)
                if packet.getPacketType() == PacketType.THROTTLE.value:
                    d_throttle = packet.getDecoded()
                    self.servoController.apply_throttle_packet(float(d_throttle))
                if packet.getPacketType() == PacketType.STABILIZATION.value:
                    stabilization = packet.getDecoded()  # 0 = off, 1 = on
                    self.servoController.auto_stabilize = int(stabilization)

            sleep(0.01)

    def send_image(self, data):
        chunk_size = 1024
        for i in range(0, len(data), chunk_size):
            self.planeTranceiver.push(b"IMAGE" + bytes(str(i), 'utf-8') + data[i:i+chunk_size])




