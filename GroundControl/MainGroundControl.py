#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be run on the ground control station

import numpy as np
import threading
import pygame
import cv2
from GroundControl.GroundCommunicationHandler import CommunicationHandler


def check_motion_keys(keys, communicationHandler, timer):
    delta_pitch = 0
    delta_yaw = 0
    delta_roll = 0
    if keys[pygame.K_w]:
        delta_pitch = -2 * pitch_coefficient
    if keys[pygame.K_a]:
        delta_yaw = -2 * yaw_coefficient
    if keys[pygame.K_s]:
        delta_pitch = 2 * pitch_coefficient
    if keys[pygame.K_d]:
        delta_yaw = 2 * yaw_coefficient
    if keys[pygame.K_q]:
        delta_roll = -2 * roll_coefficient
    if keys[pygame.K_e]:
        delta_roll = 2 * roll_coefficient
    if (delta_pitch != 0 or delta_yaw != 0 or delta_roll) and timer % 2 == 0:
        communicationHandler.send_motion(delta_pitch, delta_yaw, delta_roll)


def check_camera_keys(keys, communicationHandler, timer):
    delta_camera_pitch = 0
    delta_camera_yaw = 0
    if keys[pygame.K_UP]:
        delta_camera_pitch = -0.7
    if keys[pygame.K_DOWN]:
        delta_camera_pitch = 0.7
    if keys[pygame.K_LEFT]:
        delta_camera_yaw = 0.7
    if keys[pygame.K_RIGHT]:
        delta_camera_yaw = -0.7
    if (delta_camera_pitch != 0 or delta_camera_yaw != 0) and timer % 2 == 0:
        communicationHandler.send_camera_rotation(delta_camera_pitch, delta_camera_yaw)

def check_throttle_keys(keys, communicationHandler, timer):
    delta_throttle = 0
    if keys[pygame.K_LSHIFT]:
        delta_throttle = 1
    if keys[pygame.K_LCTRL]:
        delta_throttle = -1
    if (delta_throttle != 0) and timer % 2 == 0:
        communicationHandler.send_throttle(delta_throttle)

if __name__ == "__main__":

    communicationHandler = CommunicationHandler()

    frame = np.zeros((1280, 720, 3), dtype=np.uint8)

    UI = True

    if UI:
        pygame.init()
        window_size = (1280, 720)
        screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        pygame.display.set_caption("PiPlane Ground Control Station")
        pitch_coefficient = 1
        yaw_coefficient = 1
        roll_coefficient = 1
        mouse_pitch_coefficient = 0.25
        mouse_yaw_coefficient = 0.25

        timer = 0
        sending = False

        locked = True
        running = True
        while running:
            frame = cv2.cvtColor(communicationHandler.frame, cv2.COLOR_BGR2RGB)
            frame_rgb = pygame.surfarray.make_surface(frame)
            frame_rgb = pygame.transform.scale(frame_rgb, (1280, 720))

            x, y = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_ESCAPE:
                    #     locked = False
                    ...
                if event.type == pygame.VIDEORESIZE:
                    new_width, new_height = event.w, event.h
                    screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                if event.type == pygame.MOUSEMOTION and locked:
                    x, y = pygame.mouse.get_rel()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     locked = True

            keys = pygame.key.get_pressed()
            
            check_motion_keys(keys, communicationHandler, timer)
            check_camera_keys(keys, communicationHandler, timer)
            check_throttle_keys(keys, communicationHandler, timer)

            screen.blit(frame_rgb, (0, 0))
            timer += 1
            pygame.display.update()

        pygame.quit()
