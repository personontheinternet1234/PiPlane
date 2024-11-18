#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the pi / plane

from ServoController import ServoController
from Old.PlaneReceiver import PlaneReceiver
from Old.VideoTransmitter import VideoTransmitter

if __name__ == "__main__":
    server_ip = "192.168.1.15"
    plane_ip = "192.168.1.7"

    servoController = ServoController()
    servoController.setup_servos()
    servoController.start_threads()
    # servoController.dance()

    planeReceiver = PlaneReceiver(server_ip, plane_ip, 5559, servoController)
    planeReceiver.start_threads()

    videoTransmitter = VideoTransmitter(server_ip, 5560)
    videoTransmitter.start_threads()


