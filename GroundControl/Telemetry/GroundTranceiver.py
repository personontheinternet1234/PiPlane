import serial
from time import sleep
import queue


class GroundTranceiver:

    def __init__(self, dev='/dev/ttyUSB0', baud=57600, timeout=5, transmit_interval=0.01, receive_interval=0.01):
        self.dev = dev
        self.baud = baud

        self.transmit_interval = transmit_interval
        self.receive_interval = receive_interval
        self.transmit_queue = queue.PriorityQueue()
        self.receive_queue = queue.Queue()

        self.serial = serial.Serial(self.dev, self.baud, timeout=timeout)

    def push(self, packet, priority=0):
        self.transmit_queue.put((priority, packet))

    def pull(self):
        if self.receive_queue.qsize() > 0:
            packet = self.receive_queue.get_nowait()
            self.receive_queue.task_done()
            return packet
        return None

    def transmit(self):
        while True:

            if self.transmit_queue.qsize() > 0:
                priority, packet = self.transmit_queue.get_nowait()
                self.serial.write(packet)
                self.serial.write('\n'.encode('utf-8'))
                self.transmit_queue.task_done()

            sleep(self.transmit_interval)

    def receive(self):
        while True:
            packet = self.serial.readline()

            if packet:
                if 'test' in str(packet):
                    print('received test')
                self.receive_queue.put(packet)

            sleep(self.receive_interval)

    def AT(self, cmd):
        self.serial.write(cmd.encode('utf-8'))
        if '+++' not in cmd:
            self.serial.write('\r'.encode('utf-8'))
        else:
            sleep(1)
        sleep(0.1)

    def RSSI(self):
        self.AT('+++')
        self.AT('ATI7')
        self.AT('ATO')
        # lower |rssi| = stronger signal

    def clearTransmitQueue(self):
        while self.transmit_queue.qsize() > 0:
            try:
                self.transmit_queue.get(False)
            except Exception as e:
                print("exception")
                continue
            self.transmit_queue.task_done()

    def setConfig(self, SERIAL_SPEED=57, AIR_SPEED=64, NETID=18, TXPOWER=20, FREQ=915000, DUTY_CYCLE=100, LBT_RSSI=0, MAX_WINDOW=131):
        print('Configuring PlaneTranceiver...')
        self.AT('+++')
        self.AT(f'ATS1={SERIAL_SPEED}')
        self.AT(f'ATS2={AIR_SPEED}')
        self.AT(f'ATS3={NETID}')
        self.AT(f'ATS4={TXPOWER}')
        self.AT(f'ATS8={FREQ}')
        self.AT(f'ATS9={FREQ + 13000}')
        self.AT(f'ATS11={DUTY_CYCLE}')
        self.AT(f'ATS12={LBT_RSSI}')
        self.AT(f'ATS15={MAX_WINDOW}')
        self.AT('AT&W')
        sleep(3.5)
        self.AT('ATZ')
        print('PlaneTranceiver Configuration complete')
