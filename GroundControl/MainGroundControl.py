#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be run on the ground control station

import pygame
import numpy as np
import threading
from CommunicationHandler import CommunicationHandler


if __name__ == "__main__":

    communicationHandler = CommunicationHandler()

    temp_frame = np.zeros((1280, 720, 3), dtype=np.uint8)

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

        sending = False
        wait = 0

        locked = True
        running = True
        while running:
            frame_rgb = pygame.surfarray.make_surface(temp_frame)
            frame_rgb = pygame.transform.scale(frame_rgb, (1280, 720))

            x, y = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        locked = False
                if event.type == pygame.VIDEORESIZE:
                    new_width, new_height = event.w, event.h
                    screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    locked = True
                if event.type == pygame.MOUSEMOTION and locked:
                    x, y = pygame.mouse.get_rel()

            keys = pygame.key.get_pressed()

            if locked:
                pygame.mouse.set_visible(False)
                pygame.mouse.set_pos(screen.get_size()[0] // 2, screen.get_size()[1] // 2)
            else:
                pygame.mouse.set_visible(True)

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

            if delta_pitch != 0 or delta_yaw != 0 or delta_roll != 0:
                if wait > 20:
                    communicationHandler.send_motion(delta_pitch, delta_yaw, delta_roll)
                    wait = 0

            wait += 1

            screen.blit(frame_rgb, (0, 0))
            pygame.display.update()




        pygame.quit()
