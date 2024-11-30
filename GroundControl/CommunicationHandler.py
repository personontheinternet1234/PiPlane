import threading
from Telemetry import GroundTranceiver
from time import sleep
from GroundControl.Telemetry.GroundTranceiver import GroundTranceiver
from GroundControl.Telemetry.Packets import PacketProtocol, PacketType


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

    def listen(self):
        packet = PacketProtocol()

        while True:
            data = self.groundTranceiver.pull()
            if data is not None and packet.decode(data):
                print("received")
                if packet.getPacketType() == PacketType.MOTION.value:
                    print("Motion")
                    motion = packet.getDecoded()

            sleep(0.01)

    def send_motion(self, d_pitch, d_yaw, d_roll):
        packet = PacketProtocol(packetType=PacketType.MOTION, decoded=f"{d_pitch},{d_yaw},{d_roll}")
        self.groundTranceiver.push(packet.encode(), 0)




