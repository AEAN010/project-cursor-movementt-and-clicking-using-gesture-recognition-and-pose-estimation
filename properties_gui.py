# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:42:17 2024

@author: Anand
"""

# properties.py

import pygame
import time
# Cursor properties
screen_width = 800
screen_height = 600
cursor_x = screen_width // 2
cursor_y = screen_height // 2
prev_cursor_x = cursor_x
prev_cursor_y = cursor_y
cursor_color = (255, 255, 255)
cursor_radius = 10
cursor_speed = 0.1

# Button properties
button_x = 400
button_y = 200
button_width = 100
button_height = 50
button_color = (0, 255, 0)
button_clicked_color = (0, 0, 255)

def draw_button(screen, button_clicked):
    pygame.font.init()  # Initialize font
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Start", True, (0, 0, 0))
    button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    
    if button_clicked:
        pygame.draw.rect(screen, button_clicked_color, (button_x, button_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    screen.blit(button_text, button_text_rect)

def calculate_cursor_position(hand_x, hand_y, prev_cursor_x, prev_cursor_y, cursor_speed, cursor_radius, screen_width, screen_height):
    # Smooth cursor movement using interpolation
    cursor_x = prev_cursor_x + int((hand_x - prev_cursor_x) * cursor_speed)
    cursor_y = prev_cursor_y + int((hand_y - prev_cursor_y) * cursor_speed)

    cursor_x = max(cursor_radius, min(cursor_x, screen_width - cursor_radius))
    cursor_y = max(cursor_radius, min(cursor_y, screen_height - cursor_radius))

    return cursor_x, cursor_y


def draw_cursor(screen,cursor_x,cursor_y):
    pygame.draw.circle(screen, cursor_color, (cursor_x, cursor_y), cursor_radius)

def detect_button_click(hand_x, hand_y, button_x, button_y, button_width, button_height):
    if button_x < hand_x < button_x + button_width and button_y < hand_y < button_y + button_height:
        return True
    else:
        return False

def detect_folder_click(cursor_x, cursor_y, file_list_x, file_list_y, icon_width, icon_height):
    for i, (file_x, file_y) in enumerate(zip(file_list_x, file_list_y)):
        if (file_x - icon_width < cursor_x < file_x + icon_width) and \
           (file_y - icon_height < cursor_y < file_y + icon_height):
            return i + 1  # Return the index of the folder icon (1-based indexing)
    return None  # Return None if no collision is detected

def display_gif(screen, gif_path, x, y):
    try:
        gif = pygame.image.load(gif_path)
        screen.blit(gif, (x, y))
    except pygame.error as e:
        print("Error loading GIF:", e)


def draw_scroller(screen,cursor_x,cursor_y):

   
    pygame.draw.rect(screen, BLUE, (cursor_x, cursor_y, handle_width, handle_height))
def draw_scroll_area(screen):
    pygame.draw.rect(screen, GRAY, (scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height))

def detect_scroll_area(cursor_x, cursor_y, screen_width):
    scroll_area_width = 20  # Width of the scroll area from the right side
    scroll_area_x = screen_width - scroll_area_width  # X-coordinate of the right side of the scroll area
    
    if cursor_x >= scroll_area_x:
        return True  # Cursor is within the scroll area
    else:
        return False  # Cursor is outside the scroll area
from PIL import Image
def load_gif(filename):
    gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.convert("RGBA")  # Ensure the frame has an alpha channel
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of sequence
    return frames, gif.info['duration']
    
import sys
def display_gif():
    pygame.init()
    
    # Load GIF frames
    frames, duration = load_gif('animation1.gif')
    frame_count = len(frames)

    # Set up the display
    screen = pygame.display.set_mode(frames[0].get_size())
    pygame.display.set_caption("GIF Display")

    clock = pygame.time.Clock()
    running = True
    frame_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display the current frame
        screen.blit(frames[frame_index], (0, 0))
        pygame.display.flip()

        # Move to the next frame
        frame_index = (frame_index + 1) % frame_count

        # Control the frame rate based on the GIF's duration
        clock.tick(1000 // duration)

    pygame.quit()
    sys.exit()  
    
    
    
    
    
    
    
    
    
    
    

        
    
# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE=(0,0,255)
# Set scroll bar dimensions
scroll_bar_width = 20
scroll_bar_height = 550
scroll_bar_x = screen_width - scroll_bar_width - 10
scroll_bar_y = 100

# Set scroll bar handle dimensions
handle_width = 20
handle_height = 30
handle_x = scroll_bar_x
handle_y = scroll_bar_y
dragging_handle = False



    
    
        
    
###################################################################################################
