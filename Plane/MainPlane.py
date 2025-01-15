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
        servoController = ServoController()
        servoController.setup_servos()
        # servoController.dance()
        servoController.start_threads()

        communicationHandler = CommunicationHandler(servoController)

        IMUProcessor = IMUProcessor()
        IMUProcessor.setup()
        IMUProcessor.start_threads()

        # camera = Camera(communicationHandler)
        # camera.start_threads()
    except KeyboardInterrupt:
        print("Exiting...")
    
    # finally:
    #     if camera.cap.isOpened():
    #         camera.cap.release()

