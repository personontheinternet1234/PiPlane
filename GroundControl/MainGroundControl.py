import cv2
import pygame
import numpy as np
from GroundControlServer import ThreadedServer
import Packets
import threading

if __name__ == "__main__":
    groundControlServer = ThreadedServer("192.168.1.14", 5559)
    client_addr = "192.168.1.7"
    UI = True

    if UI:
        pygame.init()
        window_size = (640, 480)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Camera Feed with WASD and Mouse Control")
        pygame.event.set_grab(True)
        cap = cv2.VideoCapture(0)
        pitch_coefficient = 3
        yaw_coefficient = 3
        roll_coefficient = 3

        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            # convert from bgr to rgb
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = np.rot90(frame_rgb)
            frame_rgb = pygame.surfarray.make_surface(frame_rgb)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()

                keys = pygame.key.get_pressed()
                # doesnt count mouse
                if keys.__contains__(True):
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
                    groundControlServer.send_packet_to(client_addr, Packets.MotionPacket(delta_pitch, delta_yaw, delta_roll))

                # if event.type == pygame.MOUSEMOTION:
                #     x, y = pygame.mouse.get_rel()

            # display camera on window
            screen.blit(frame_rgb, (0, 0))
            pygame.display.update()

        cap.release()
        pygame.quit()
