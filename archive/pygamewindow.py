import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the window
# width, height = 500, 500
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.font.init() # you have to call this at the start if you want to use the module
clock = pygame.time.Clock()
padding = 100
# Setup the display
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
windowX, windowY = displayX - 100, displayY - 100 #windowX, windowY = displayX - 100, displayY - 100
screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window")

# Set up the square
square_color = (255, 0, 0)
min_margin = 20  # Set your desired minimum margin
square_size = min(windowX, windowY) - 2 * min_margin
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            windowX, windowY = event.w, event.h
            screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
            square_size = min(windowX, windowY) - 2 * min_margin
            square_rect.x = (windowX - square_size) // 2
            square_rect.y = (windowY - square_size) // 2
            square_rect.width = square_size
            square_rect.height = square_size

    # Draw background
    screen.fill((255, 255, 255))

    # Draw the square
    pygame.draw.rect(screen, square_color, square_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)