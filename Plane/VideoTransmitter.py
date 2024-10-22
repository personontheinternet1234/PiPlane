import cv2
import socket
import struct
import pickle
import threading
from picamera2 import Picamera2

class VideoTransmitter:

    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration())

    def start_threads(self):
        threading.Thread(target=self.start_transmission).start()

    def start_transmission(self):
        self.camera.start()
        while True:
            frame = self.camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            self.client_socket.sendto(buffer, (self.server_ip, self.port))

        self.client_socket.close()
        self.camera.stop()

if __name__ == "__main__":
    server_ip = "192.168.1.14"
    videoTransmitter = VideoTransmitter(server_ip, 5560)
    videoTransmitter.start_transmission()
