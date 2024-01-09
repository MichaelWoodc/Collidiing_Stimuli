import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def draw_balls(balls):
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball['radius'])

def move_balls(balls):
    for ball in balls:
        ball['x'] += ball['speed'][0]
        ball['y'] += ball['speed'][1]

        # Bounce off walls
        if ball['x'] - ball['radius'] <= 0 or ball['x'] + ball['radius'] >= WIDTH:
            ball['speed'][0] = -ball['speed'][0]
        if ball['y'] - ball['radius'] <= 0 or ball['y'] + ball['radius'] >= HEIGHT:
            ball['speed'][1] = -ball['speed'][1]

def main(balls):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_balls(balls)

        # Clear the screen
        screen.fill(WHITE)

        draw_balls(balls)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    # Example dictionary with information about balls
    balls_info = [
        {'x': 100, 'y': 100, 'radius': 20, 'color': (255, 0, 0), 'speed': [5, 3]},
        {'x': 200, 'y': 200, 'radius': 15, 'color': (0, 255, 0), 'speed': [-4, 2]},
        {'x': 300, 'y': 300, 'radius': 25, 'color': (0, 50, 255), 'speed': [2, -4]},
        {'x': 300, 'y': 300, 'radius': 25, 'color': (0, 0, 255), 'speed': [3, -5]}
        # Add more balls as needed
    ]

    balls = balls_info

    main(balls)