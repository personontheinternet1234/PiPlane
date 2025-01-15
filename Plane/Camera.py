import cv2
import numpy as np
import threading
from time import sleep
from PlaneCommunicationHandler import CommunicationHandler

class Camera:

    def __init__(self, communicationHandler):
        self.cap = cv2.VideoCapture(0)
        self.planeCommunicationHandler = communicationHandler

    def start_threads(self):
        threading.Thread(target=self.camera_loop).start()

    def camera_loop(self):
        while True:
            self.take_picture_and_send()
            sleep(1000)
    
    def take_picture_and_send(self):
        ret, frame = self.cap.read()

        if ret:
            decreased = cv2.cvtColor(cv2.resize(frame, (320, 240)), cv2.COLOR_BGR2GRAY)
            _, buffer = cv2.imencode('.jpg', decreased, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
            image_bytes = buffer.tobytes()

            self.planeCommunicationHandler.send_image(image_bytes)
        else:
            print("Camera Error - Can't find it?")

    def release(self):
        self.cap.release()