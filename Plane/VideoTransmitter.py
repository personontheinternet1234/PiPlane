import cv2
import socket
import struct
import pickle
import threading
import time
from picamera2 import Picamera2

class VideoTransmitter:

    def __init__(self, server_ip, port, fps=10):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.fps = fps
        self.frame_interval = 1 / fps

        self.camera = Picamera2()
        camera_config = self.camera.create_preview_configuration(
            main={"size": (320, 240)},
            lores={"size": (160, 120), "format": "YUV420"}
        )
        self.camera.configure(camera_config)

    def start_threads(self):
        threading.Thread(target=self.start_transmission).start()

    def start_transmission(self):
        self.camera.start()
        last_frame_time = 0

        while True:
            current_time = time.time()
            if current_time - last_frame_time < self.frame_interval:
                continue

            frame = self.camera.capture_array()
            _, buffer = cv2.imencode('.jpg', cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE), [cv2.IMWRITE_JPEG_QUALITY, 30])
            self.client_socket.sendto(buffer, (self.server_ip, self.port))

            last_frame_time = current_time

        self.client_socket.close()
        self.camera.stop()

if __name__ == "__main__":
    server_ip = "192.168.1.14"
    videoTransmitter = VideoTransmitter(server_ip, 5560, fps=30)
    videoTransmitter.start_transmission()
