import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create an initial window
width, height = 400, 400
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("TEST")

# Initial position and size of the square
square_size = min(width, height) // 2
square_rect = pygame.Rect((width - square_size) // 2, (height - square_size) // 2, square_size, square_size)

def bounce():
    pass
def drawToDisplaySize():
    global width, height, square_rect, square_size
    # Update the window size
    width, height = event.w, event.h
    # Update the size of the square based on the new window size
    square_size = min(width, height) // 2
    square_rect.size = (square_size, square_size)
    # Update the position of the square to keep it centered
    square_rect.x = (width - square_size) // 2
    square_rect.y = (height - square_size) // 2

# drawToDisplaySize()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            drawToDisplaySize()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the square
    pygame.draw.rect(screen, BLACK, square_rect)

    # Update the display
    pygame.display.flip()