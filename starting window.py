# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:44:07 2024

@author: Anand
"""
import pygame
import cv2
import mediapipe as mp
from properties_gui import *
from pred_gesture_utils import *
from new_screen_main import *
import subprocess
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game with Boundary")


image=r"house.jpg"###################################################################



#######################################################################
button_click=False
# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
connections = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10],
               [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18], [18, 19], [19, 20]]

button_clicked=False

running = True
cap = cv2.VideoCapture(0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    hand_frame=None
    hand_flag=False
    cursor_pass_x = None
    curor_pass_y =None 
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_x = int(hand_landmarks.landmark[8].x * screen_width)
            hand_y = int(hand_landmarks.landmark[8].y * screen_height)
              
            hand_frame=hand_landmarks
            hand_flag=True
            # Check if the hand is pointing inside the button area
           
           
            
            cursor_x, cursor_y = calculate_cursor_position(hand_x, hand_y, prev_cursor_x, prev_cursor_y,
                                                           cursor_speed, cursor_radius, screen_width, screen_height)

            button_clicked = detect_button_click(cursor_x, cursor_y, button_x, button_y, button_width, button_height)
            
            draw_cursor(screen, cursor_x, cursor_y)
            cursor_pass_x=cursor_x
            cursor_pass_y=cursor_y
            # Update previous cursor position
            prev_cursor_x = cursor_x
            prev_cursor_y = cursor_y
            
                
                
                
            
            
    else:
        # If hand position is not detected, keep the cursor at its previous location
        draw_cursor(screen, prev_cursor_x, prev_cursor_y)

    # Draw the button
    if button_clicked and hand_flag==True:
       hand_flag=False
        
       flag= predict_model(frame, hand_frame)
       if flag==2:
           subprocess.Popen(["python", "folder_screen.py", str(cursor_pass_x), str(cursor_pass_y)])
           running=False
       
    draw_button(screen, button_clicked)

    pygame.display.flip()

cap.release()
pygame.quit()
