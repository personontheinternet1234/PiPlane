#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the pi / plane

import threading
from ServoController import ServoController
from CommunicationHandler import CommunicationHandler
from time import sleep

if __name__ == "__main__":
    servoController = ServoController()
    servoController.setup_servos()
    # servoController.dance()
    servoController.start_threads()

    communicationHandler = CommunicationHandler(servoController)



