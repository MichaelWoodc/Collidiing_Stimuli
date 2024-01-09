import pygame
import random
import math
import tkinter as tk
from tkinter import ttk
import time
import csv

######################################################################################################
########################################### Dr, Randall's Variables ##################################
######################################################################################################

change_over_delay_between_balls = 3
change_over_delay_countdown = 0
opportunity_to_score = True
BALL_RADIUS = 50
ball_1_speed_x = 0.05
ball_1_speed_y = 0.08
ball_2_speed_x = 0.08
ball_2_speed_y = 0.05

fixed_ratio_responses_ball_1 = 2
fixed_ratio_responses_ball_2 = 2

fixed_ratio = True
last_ball_to_score = 0


# CSV file handling
csv_file_path = 'game_data.csv'
def write_to_csv(data):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        
# Function to update the values based on user input      
def update_values():
    global BALL_RADIUS, ball_1_speed_x, ball_1_speed_y, ball_2_speed_x, ball_2_speed_y
    global change_over_delay_between_balls, fixed_ratio_responses_ball_1, reinforcement_method_var

    BALL_RADIUS = int(ball_radius_var.get())
    ball_1_speed_x = float(ball_1_speed_x_var.get())
    ball_1_speed_y = float(ball_1_speed_y_var.get())
    ball_2_speed_x = float(ball_2_speed_x_var.get())
    ball_2_speed_y = float(ball_2_speed_y_var.get())
    change_over_delay_between_balls = int(change_over_delay_var.get())
    fixed_ratio_responses_ball_1 = int(fixed_ratio_responses_var.get())

    # Create the reinforcement_method_var inside the function
    reinforcement_method_var = tk.StringVar()
    reinforcement_method_var.set(reinforcement_method_menu.get())  # Set the selected value

    # Close the settings window
    write_to_csv(["Setting Updated", time.strftime("%Y-%m-%d %H:%M:%S")])

    settings_window.destroy()


# Create the Tkinter window
settings_window = tk.Tk()
settings_window.title("Bouncing Balls Settings")

# Ball Radius
ball_radius_label = ttk.Label(settings_window, text="Ball Radius:")
ball_radius_label.grid(row=0, column=0, padx=10, pady=5)
ball_radius_var = tk.StringVar()
ball_radius_entry = ttk.Entry(settings_window, textvariable=ball_radius_var)
ball_radius_entry.grid(row=0, column=1, padx=10, pady=5)
ball_radius_var.set(str(BALL_RADIUS))

# Ball 1 Speed X
ball_1_speed_x_label = ttk.Label(settings_window, text="Ball 1 Speed X:")
ball_1_speed_x_label.grid(row=1, column=0, padx=10, pady=5)
ball_1_speed_x_var = tk.StringVar()
ball_1_speed_x_entry = ttk.Entry(settings_window, textvariable=ball_1_speed_x_var)
ball_1_speed_x_entry.grid(row=1, column=1, padx=10, pady=5)
ball_1_speed_x_var.set(str(ball_1_speed_x))

# Ball 1 Speed Y
ball_1_speed_y_label = ttk.Label(settings_window, text="Ball 1 Speed Y:")
ball_1_speed_y_label.grid(row=2, column=0, padx=10, pady=5)
ball_1_speed_y_var = tk.StringVar()
ball_1_speed_y_entry = ttk.Entry(settings_window, textvariable=ball_1_speed_y_var)
ball_1_speed_y_entry.grid(row=2, column=1, padx=10, pady=5)
ball_1_speed_y_var.set(str(ball_1_speed_y))

# Ball 2 Speed X
ball_2_speed_x_label = ttk.Label(settings_window, text="Ball 2 Speed X:")
ball_2_speed_x_label.grid(row=3, column=0, padx=10, pady=5)
ball_2_speed_x_var = tk.StringVar()
ball_2_speed_x_entry = ttk.Entry(settings_window, textvariable=ball_2_speed_x_var)
ball_2_speed_x_entry.grid(row=3, column=1, padx=10, pady=5)
ball_2_speed_x_var.set(str(ball_2_speed_x))

# Ball 2 Speed Y
ball_2_speed_y_label = ttk.Label(settings_window, text="Ball 2 Speed Y:")
ball_2_speed_y_label.grid(row=4, column=0, padx=10, pady=5)
ball_2_speed_y_var = tk.StringVar()
ball_2_speed_y_entry = ttk.Entry(settings_window, textvariable=ball_2_speed_y_var)
ball_2_speed_y_entry.grid(row=4, column=1, padx=10, pady=5)
ball_2_speed_y_var.set(str(ball_2_speed_y))

# Change-over Delay
change_over_delay_label = ttk.Label(settings_window, text="Change-over Delay:")
change_over_delay_label.grid(row=5, column=0, padx=10, pady=5)
change_over_delay_var = tk.StringVar()
change_over_delay_entry = ttk.Entry(settings_window, textvariable=change_over_delay_var)
change_over_delay_entry.grid(row=5, column=1, padx=10, pady=5)
change_over_delay_var.set(str(change_over_delay_between_balls))

# Fixed Ratio Responses Ball 1
fixed_ratio_responses_label = ttk.Label(settings_window, text="Fixed Ratio Responses Ball 1:")
fixed_ratio_responses_label.grid(row=6, column=0, padx=10, pady=5)
fixed_ratio_responses_var = tk.StringVar()
fixed_ratio_responses_entry = ttk.Entry(settings_window, textvariable=fixed_ratio_responses_var)
fixed_ratio_responses_entry.grid(row=6, column=1, padx=10, pady=5)
fixed_ratio_responses_var.set(str(fixed_ratio_responses_ball_1))

# Button to update values
update_button = ttk.Button(settings_window, text="Update Values", command=update_values)
update_button.grid(row=7, column=0, columnspan=2, pady=10)

# Reinforcement Method Drop-down menu
reinforcement_method_label = ttk.Label(settings_window, text="Reinforcement Method:")
reinforcement_method_label.grid(row=8, column=0, padx=10, pady=5)
reinforcement_method_menu = ttk.Combobox(settings_window,
                                         values=["Fixed Ratio", "Other Method 1", "Other Method 2"])
reinforcement_method_menu.grid(row=8, column=1, padx=10, pady=5)

# Start the Tkinter main loop
settings_window.mainloop()

# Initialize Pygame
pygame.init()
# Create the screen in full-screen mode
#screen = pygame.display.set_mode((500, 500)) #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("Bouncing Balls")

# ######################################################################################################
# ########################################### Dr, Randall's Variables ##################################
# ###################################################################################################### 


SQUARE_WIDTH = WIDTH - 300 #700  # Added SQUARE_SIZE
SQUARE_HEIGHT = HEIGHT - 100 #500  # Added SQUARE_SIZE
SQUARE_COLOR = (255, 255, 255)
SQUARE_THICKNESS = 4
PADDING = 50  # Padding value for centering the square

ball_click_color_time = 0.05 # seconds to change ball color after 1 click

# Load images and scale them while maintaining aspect ratio
max_image_width = 200  # Maximum width for the scaled images
left_image = pygame.image.load("motorcycle.png")  # Replace with the path to your left image
right_image = pygame.image.load("tswift.png")  # Replace with the path to your right image

# Constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 255, 0)

BALL_1_COLOR, BALL_1_CLICKED_COLOR = BLUE, DARK_BLUE
BALL_2_COLOR,BALL_2_CLICKED_COLOR = YELLOW, DARK_YELLOW

# initialize to a large negative value to ensure that the score can be updated right away
last_point_ball_1, last_click_ball_1, last_point_ball_2, last_click_ball_2 = -10000, -10000, -10000, -10000
last_ball_click = 0
fixed_ratio_counter_ball_1 = 0
fixed_ratio_counter_ball_2 = 0
last_clicked_ball = 0
block_change_until = 0
clickedball = 0
# Counter variables
click_count_ball_1, score_count_ball_1, fixed_ratio_counter_ball_1, click_count_ball_2, score_count_ball_2,fixed_ratio_counter_ball_2 = 0, 0, 0, 0, 0, 0
ball_counter_end = 0
# Scale the images based on the maximum width while maintaining aspect ratio
def scale_image(image, max_width):
    ratio = max_width / image.get_width()
    new_height = int(image.get_height() * ratio)
    return pygame.transform.scale(image, (max_width, new_height))

def ball_handling():
    global last_click_ball_1, last_click_ball_2, ball_1, ball_2
    
    if clickedball == 1:
        # last_click_ball_1 = current_time
        ball_1['color'] = BALL_1_CLICKED_COLOR# change color based on formula(ball_1['color'][0], ball_1['color'][1], ball_1['color'][2]-50)
        
    if current_time > last_click_ball_1 + ball_click_color_time * 1000:
        ball_1['color'] = BALL_1_COLOR
        
    if clickedball == 2:
        # last_click_ball_2 = current_time
        ball_2['color'] = BALL_2_CLICKED_COLOR #(ball_2['color'][0], ball_2['color'][1], ball_2['color'][2]-50)
    if current_time > last_click_ball_2 + ball_click_color_time * 1000:
        ball_2['color'] = BALL_2_COLOR
        
# if update_position == True:
    # Update ball positions
    ball_1['x'] += ball_1['dx']
    ball_1['y'] += ball_1['dy']
    ball_2['x'] += ball_2['dx']
    ball_2['y'] += ball_2['dy']

    # Bounce off the border of the white square for both balls
    if ball_1['x'] - BALL_RADIUS < square_x or ball_1['x'] + BALL_RADIUS > square_x + SQUARE_WIDTH:
        ball_1['dx'] *= -1
    if ball_1['y'] - BALL_RADIUS < square_y or ball_1['y'] + BALL_RADIUS > square_y + SQUARE_HEIGHT:
        ball_1['dy'] *= -1

    if ball_2['x'] - BALL_RADIUS < square_x or ball_2['x'] + BALL_RADIUS > square_x + SQUARE_WIDTH:
        ball_2['dx'] *= -1
    if ball_2['y'] - BALL_RADIUS < square_y or ball_2['y'] + BALL_RADIUS > square_y + SQUARE_HEIGHT:
        ball_2['dy'] *= -1
        # Draw the balls
    pygame.draw.circle(screen, ball_1['color'], (ball_1['x'], ball_1['y']), BALL_RADIUS)
    pygame.draw.circle(screen, ball_2['color'], (ball_2['x'], ball_2['y']), BALL_RADIUS)

def change_over_countdown():
    global last_ball_to_score, change_over_delay_countdown, last_ball_click_time, block_change_until
    if clickedball != 0:
        if last_ball_to_score == clickedball:
            block_change_until = (change_over_delay_between_balls * 1000) + current_time
            print('Breakpoint')
        else:
            last_ball_click_time = current_time
    # change_over_delay_countdown =  (change_over_delay_between_balls * 1000)# - current_time
        print('breakpoint')


left_image = scale_image(left_image, max_image_width)
right_image = scale_image(right_image, max_image_width)

# Calculate the square's position to center it on the screen
square_x = (WIDTH - SQUARE_WIDTH) // 2
square_y = (HEIGHT - SQUARE_HEIGHT) // 2

# Calculate image positions
left_image_x = square_x - left_image.get_width()
right_image_x = square_x + SQUARE_WIDTH

# Initialize ball properties within the square
ball_1 = {
    'x': random.randint(square_x + BALL_RADIUS, square_x + SQUARE_WIDTH - BALL_RADIUS),
    'y': random.randint(square_y + BALL_RADIUS, square_y + SQUARE_HEIGHT - BALL_RADIUS),
    'dx': ball_1_speed_x,  
    'dy': ball_1_speed_y,  
    'color': BALL_1_COLOR
}

ball_2 = {
    'x': random.randint(square_x + BALL_RADIUS, square_x + SQUARE_WIDTH - BALL_RADIUS),
    'y': random.randint(square_y + BALL_RADIUS, square_y + SQUARE_HEIGHT - BALL_RADIUS),
    'dx': ball_2_speed_x,  
    'dy': ball_2_speed_y,  
    'color': BALL_2_COLOR
}


font = pygame.font.Font(None, 36)  # Choose a font and size

######################### Game loop #########################
running = True
   

while running:
    clickedball = 0
    current_time = pygame.time.get_ticks()
    # change_over_delay_countdown = block_change_until - current_time
    if block_change_until - current_time <= 0:
        change_over_delay_countdown = None
        pass
    else:
        change_over_delay_countdown = block_change_until - current_time
        pass
        # change_over_delay_countdown = min(((last_click_ball_1 + change_over_delay_between_balls * 1000)- current_time),(last_click_ball_2 + change_over_delay_between_balls * 1000)- current_time)

    opportunity_to_score = True
    for event in pygame.event.get():        

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            ########### BALL 1 CODE ####################
            if math.hypot(x - ball_1['x'], y - ball_1['y']) <= BALL_RADIUS:
                last_ball_click_time = current_time
                click_count_ball_1 += 1
                clickedball=1
                change_over_countdown()
                ball_handling()
                # Update CSV file with click data
                write_to_csv(["Ball 1 Click", click_count_ball_1, score_count_ball_1, time.strftime("%Y-%m-%d %H:%M:%S")])
                
                if current_time > last_point_ball_2 + change_over_delay_between_balls * 1000:
                    last_point_ball_1 = current_time
                                        
                    if fixed_ratio == True:
                        fixed_ratio_counter_ball_1 += 1
                        
                        if fixed_ratio_counter_ball_1 == fixed_ratio_responses_ball_1:
                            fixed_ratio_counter_ball_1 = 0
                            score_count_ball_1 += 1
                            last_ball_to_score = 1

                        continue
                    score_count_ball_1 += 1

            ########### BALL 2 CODE ####################  
            if math.hypot(x - ball_2['x'], y - ball_2['y']) <= BALL_RADIUS:
                last_ball_click_time = current_time    
                clickedball=2
                change_over_countdown()
                click_count_ball_2 += 1
                
                ball_handling()
                if current_time > last_point_ball_1 + change_over_delay_between_balls * 1000:
                    last_point_ball_2 = current_time                
                    
                    if fixed_ratio == True:
                        fixed_ratio_counter_ball_2 += 1
                        
                        if fixed_ratio_counter_ball_2 == fixed_ratio_responses_ball_1:
                            print('Able to increment score')
                            score_count_ball_2 += 1
                            fixed_ratio_counter_ball_2 = 0
                            last_ball_to_score = 2
                        continue
                    score_count_ball_2 += 1


    # Fill the screen with a black background
    screen.fill(BLACK)
    ball_handling() # must be called after filling in screen
    
    # Blit the images
    screen.blit(left_image, (left_image_x, (HEIGHT - left_image.get_height()) // 2))
    screen.blit(right_image, (right_image_x, (HEIGHT - right_image.get_height()) // 2))

    # Draw the white square outline
    pygame.draw.rect(screen, SQUARE_COLOR, (square_x, square_y, SQUARE_WIDTH, SQUARE_HEIGHT), SQUARE_THICKNESS)
    # pygame.draw.circle(screen, ball_1['color'], (ball_1['x'], ball_1['y']), BALL_RADIUS)
    # pygame.draw.circle(screen, ball_2['color'], (ball_2['x'], ball_2['y']), BALL_RADIUS)
    # Draw the click counters
    text_ball_1 = font.render(f'Ball 1 Clicks: {click_count_ball_1} Ball 1 score {score_count_ball_1}', True, BALL_1_COLOR)
    text_ball_2 = font.render(f'Yellow Clicks: {click_count_ball_2} Ball 2 score {score_count_ball_2}', True, YELLOW)
    text_rect_ball_1 = text_ball_1.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    text_rect_ball_2 = text_ball_2.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text_ball_1, text_rect_ball_1)
    screen.blit(text_ball_2, text_rect_ball_2)
    
    #template to add more text
    # text = font.render(f'change_over_delay_countdown: {change_over_delay_countdown}', True, YELLOW)
    # change_over_delay_countdown
    change_over_countdown()
    # if change_over_delay_countdown < 0:
    #     pass
    # else:
    text_change_over_delay = font.render(f'Change over delay timer: {change_over_delay_countdown}', True, YELLOW)
    text_rect = text_change_over_delay.get_rect(center=(WIDTH // 2, HEIGHT - 10))
    screen.blit(text_change_over_delay, text_rect)

    # #template to add more text
    # text = font.render(f'Yellow Clicks: {click_count_ball_2} Ball 2 score {score_count_ball_2}', True, YELLOW)
    # text_rect_change_over_timer = text_ball_2.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    # screen.blit(text_ball_1, text_rect_ball_1)

    pygame.display.update()

# Quit Pygame
pygame.quit()