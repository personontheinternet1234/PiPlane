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
    server_ip = "192.168.1.15"
    plane_ip = "192.168.1.7"

    servoController = ServoController()
    servoController.setup_servos()
    servoController.start_threads()

    communicationHandler = CommunicationHandler(servoController)




