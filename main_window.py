# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:52:58 2024

@author: Anand
"""
# subprocess_window.py

# subprocess_window.py

import pygame
import sys
import cv2
import mediapipe as mp
from properties_gui import *
from pred_gesture_utils import *
import subprocess
import sys



# Initialize Pygame
pygame.init()


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game with Boundary")

# Get cursor position from command-line arguments
if len(sys.argv) >= 3:
    cursor_x = int(sys.argv[1])
    cursor_y = int(sys.argv[2])
else:
    cursor_x = screen_width // 2
    cursor_y = screen_height // 2

cursor_radius = 10
cursor_color = (255, 255, 255)

# Load folder icon image
folder_icon = pygame.image.load("folder_icon.jpg")  # Replace "folder_icon.png" with your file path
img = pygame.image.load("house.jpg")
img2 = pygame.image.load("animation1.gif")
img_path=img
# Initialize folder icon positions
file1_x = 100
file1_y = 100

file2_x = 300
file2_y = 100

file3_x = 500
file3_y = 100


file_list_x=[file1_x,file2_x,file3_x]
file_list_y=[file1_y,file2_y,file3_y]
stop_folder=1
cap=cv2.VideoCapture(0)
# Main game loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    stop_folder=1
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
            hand_x = int(hand_landmarks.landmark[7].x * screen_width)
            hand_y = int(hand_landmarks.landmark[7].y * screen_height)
              
            hand_frame=hand_landmarks
            hand_flag=True
       
            
            cursor_x, cursor_y = calculate_cursor_position(hand_x, hand_y, prev_cursor_x, prev_cursor_y,
                                                           cursor_speed, cursor_radius, screen_width, screen_height)

            
            button_clicked = detect_folder_click(cursor_x,cursor_y, file_list_x,file_list_y,90,90)
            scroll_detect=detect_scroll_area(cursor_x,cursor_y, screen_width)
     
            
            if scroll_detect:
                
                draw_scroller(screen, cursor_x, cursor_y)
            else:
                draw_cursor(screen, cursor_x, cursor_y)
            cursor_pass_x=cursor_x
           
            cursor_pass_y=cursor_y
            
           
            
           # Update previous cursor position
            prev_cursor_x = cursor_x
            prev_cursor_y = cursor_y
            
            ##############################################33
            if button_clicked==2: # 2 ,means file no 2
                flag=predict_model(frame, hand_landmarks)
                if flag==2:
                    #screen.blit(img,(0,0))
                    stop_folder=0
                    screen.fill((0, 0, 0))
                    screen.blit(img,(0,0))
                    
                    #subprocess.Popen(["python","screen_load.py",str(img_path),str(what_to_do_idx)])
            ###### button 2 clicked and prediction
            if button_clicked==1:
                flag=predict_model(frame, hand_landmarks)
                if flag==2:
                   display_gif()
                
            ######################################################3    
                
            
            
    else:
        # If hand position is not detected, keep the cursor at its previous location
        draw_cursor(screen, prev_cursor_x, prev_cursor_y)
    
    
    

    
    

    # Draw folder icons and file names
    if stop_folder !=0:
         
       
        screen.blit(folder_icon, (file1_x, file1_y))
        screen.blit(folder_icon, (file2_x, file2_y))
        screen.blit(folder_icon, (file3_x, file3_y))
    
    # Render and display file names
        font = pygame.font.Font(None, 24)  # Set the font and size
        file1_text = font.render("Animation_gif", True, (255, 255, 255))  # Replace "File 1" with your file name
        file2_text = font.render("hoise_img", True, (255, 255, 255))  # Replace "File 2" with your file name
        file3_text = font.render("void", True, (255, 255, 255))  # Replace "File 3" with your file name
        screen.blit(file1_text, (file1_x + 20, file1_y + folder_icon.get_height() + 5))  # Adjust position as needed
        screen.blit(file2_text, (file2_x + 20, file2_y + folder_icon.get_height() + 5))  # Adjust position as needed
        screen.blit(file3_text, (file3_x + 20, file3_y + folder_icon.get_height() + 5))  # Adjust position as needed

    draw_scroll_area(screen)
    
    
    
    
    
    
    
    pygame.draw.circle(screen, cursor_color, (cursor_x, cursor_y), cursor_radius)

    pygame.display.flip()

pygame.quit()
cap.release()