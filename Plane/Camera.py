import cv2
import numpy as np
import threading
from time import sleep

class Camera:

    def __init__(self, communicationHandler):
        self.cap = cv2.VideoCapture(0)
        self.planeCommunicationHandler = communicationHandler

    def start_threads(self):
        threading.Thread(target=self.camera_loop).start()

    def camera_loop(self):
        while True:
            sleep(0.5)
            self.take_picture_and_send()
    
    def take_picture_and_send(self):
        ret, frame = self.cap.read()
        self.cap.release()

        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()

            self.planeCommunicationHandler.send_image(image_bytes)
        else:
            print("Camera Error - Can't find it?")
