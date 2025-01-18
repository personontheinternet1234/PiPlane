#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the pi / plane

import threading
from ServoController import ServoController
from PlaneCommunicationHandler import CommunicationHandler
from IMU.IMUProcessor import IMUProcessor
from Navigation.I2CGPS import I2CGPS
from Navigation.NavigationManager import NavigationManager
from FlightTracker import FlightTracker
from Camera import Camera
from time import sleep

if __name__ == "__main__":
    try:
        imu = IMUProcessor()
        imu.setup()
        imu.start_threads()

        servoController = ServoController(imu)
        servoController.setup_servos()
        servoController.start_threads()

        communicationHandler = CommunicationHandler(servoController)

        # gps = I2CGPS()
        # gps.start_threads()

        # navigationManager = NavigationManager(servoController, imu, gps)
        # navigationManager.start_threads()

        # flightTracker = FlightTracker(imu, gps)
        # flightTracker.start_threads()

        # camera = Camera(communicationHandler)
        # camera.start_threads()
    except KeyboardInterrupt:
        print("Exiting...")
        # if camera.cap.isOpened():
        #     camera.cap.release()



