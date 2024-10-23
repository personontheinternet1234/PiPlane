import cv2
import socket
import numpy as np
import threading


class VideoReceiver:


    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.frame = np.zeros((400, 400, 3), dtype=np.uint8)

    def start_threads(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        while True:
            data, addr = self.server_socket.recvfrom(65535)

            np_data = np.frombuffer(data, dtype=np.uint8)
            self.frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        cv2.destroyAllWindows()
        self.server_socket.close()
