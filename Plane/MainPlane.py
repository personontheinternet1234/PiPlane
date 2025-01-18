#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the pi / plane

import threading
from ServoController import ServoController
from PlaneCommunicationHandler import CommunicationHandler
from IMU.IMUProcessor import IMUProcessor
from Camera import Camera
from time import sleep

if __name__ == "__main__":
    try:
        IMU = IMUProcessor()
        IMU.setup()
        IMU.start_threads()

        servoController = ServoController(IMU)
        servoController.setup_servos()
        servoController.start_threads()

        communicationHandler = CommunicationHandler(servoController)

        # camera = Camera(communicationHandler)
        # camera.start_threads()
    except KeyboardInterrupt:
        print("Exiting...")
        # if camera.cap.isOpened():
        #     camera.cap.release()



