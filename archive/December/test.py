import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the width and height of the window
window_width = 800
window_height = 600

# Create the Pygame window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Images Inside Rectangle")

# Define rectangle parameters
rectangle_width = 200
rectangle_height = 400
rectangle_color = (0, 0, 255)  # Blue

# Create a rectangle surface
rectangle_surface = pygame.Surface((rectangle_width, rectangle_height))
rectangle_surface.fill(rectangle_color)

# Load images
image_path1 = "test1.png"
image_path2 = "test2.png"
image1 = pygame.image.load(image_path1)
image2 = pygame.image.load(image_path2)

# Get original image dimensions
original_image1_width, original_image1_height = image1.get_size()
original_image2_width, original_image2_height = image2.get_size()

# Calculate scale factors for resizing images to fit within the rectangle
scale_factor1 = min(rectangle_width / original_image1_width, rectangle_height / original_image1_height)
scale_factor2 = min(rectangle_width / original_image2_width, rectangle_height / original_image2_height)

# Resize images
image1 = pygame.transform.scale(image1, (int(original_image1_width * scale_factor1), int(original_image1_height * scale_factor1)))
image2 = pygame.transform.scale(image2, (int(original_image2_width * scale_factor2), int(original_image2_height * scale_factor2)))

# Calculate positions for images
image1_x = (window_width - rectangle_width) // 2 - image1.get_width()
image1_y = (window_height - image1.get_height()) // 2

image2_x = (window_width + rectangle_width) // 2
image2_y = (window_height - image2.get_height()) // 2

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the rectangle
    screen.blit(rectangle_surface, ((window_width - rectangle_width) // 2, (window_height - rectangle_height) // 2))

    # Blit the images onto the screen
    screen.blit(image1, (image1_x, image1_y))
    screen.blit(image2, (image2_x, image2_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
