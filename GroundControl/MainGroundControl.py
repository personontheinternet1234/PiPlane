import cv2
import pygame
import numpy as np
import socket

pygame.init()
window_size = (640, 480)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Camera Feed with WASD and Mouse Control")
pygame.event.set_grab(True)
cap = cv2.VideoCapture(0)

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
            if event.key == pygame.K_w:
                print("W pressed")
            elif event.key == pygame.K_a:
                print("A pressed")
            elif event.key == pygame.K_s:
                print("S pressed")
            elif event.key == pygame.K_d:
                print("D pressed")
            elif event.key == pygame.K_q:
                print("Q pressed")
            elif event.key == pygame.K_e:
                print("E pressed")
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_rel()
            # print(f"Mouse moved: {x}, {y}")

    # display camera on window
    screen.blit(frame_rgb, (0, 0))
    pygame.display.update()

cap.release()
pygame.quit()
