#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: October 17, 2024
# Project: PiPlane
# Purpose: Main script to be ran on the ground control station

import pygame
from Old.GroundControlServer import ThreadedServer
from VideoReceiver import VideoReceiver
import Packets

if __name__ == "__main__":
    host_addr = "192.168.1.15"
    client_addr = "192.168.1.7"

    groundControlServer = ThreadedServer(host_addr, 5559)

    videoReceiver = VideoReceiver(host_addr, 5560)
    videoReceiver.start_threads()

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


            # convert from bgr to rgb
            frame_rgb = videoReceiver.frame
            frame_rgb = pygame.surfarray.make_surface(frame_rgb)
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

            if (delta_pitch != 0 or delta_yaw != 0 or delta_roll != 0):
                if wait > 20:
                    # groundControlServer.send_packet_to(client_addr, Packets.MotionPacket(delta_pitch, delta_yaw, delta_roll))
                    groundControlServer.send_packet_to(client_addr, Packets.TestPacket())
                    wait = 0

            wait += 1

            # display camera on window
            screen.blit(frame_rgb, (0, 0))
            pygame.display.update()

        pygame.quit()
