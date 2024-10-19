import cv2
import socket
import struct
import pickle
import threading

class VideoTransmitter:

    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_threads(self):
        threading.Thread(target=self.start_transmission).start()

    def start_transmission(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("errror")
                break

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])

            self.client_socket.sendto(buffer, (self.server_ip, self.port))
            cv2.imshow('Video Stream', frame)

        cap.release()
        self.client_socket.close()

if __name__ == "__main__":
    server_ip = "192.168.1.14"
    videoTransmitter = VideoTransmitter(server_ip, 5560)
    videoTransmitter.start_transmission()
