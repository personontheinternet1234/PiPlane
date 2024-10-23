#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the pi / plane

from ServoController import ServoController
from PlaneReceiver import PlaneReceiver
from VideoTransmitter import VideoTransmitter

if __name__ == "__main__":
    servoController = ServoController()
    servoController.setup_servos()
    servoController.start_threads()
    # servoController.dance()

    server_ip = "192.168.1.14"
    planeReceiver = PlaneReceiver(server_ip, 5559, servoController)
    planeReceiver.start_threads()

    videoTransmitter = VideoTransmitter(server_ip, 5560, fps=30)
    videoTransmitter.start_threads()

    # pi.set_servo_pulsewidth(servo_pin, 0) 
    # pi.stop()


