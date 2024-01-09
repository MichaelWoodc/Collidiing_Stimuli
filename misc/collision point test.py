import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Collision with Mouse")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.radius = radius
        self.rect = self.image.get_rect(center=(x, y))

def find_intersection(circle1, circle2):
    # Calculate the vector between the centers of the circles
    distance_vector = pygame.math.Vector2(circle2.rect.center) - pygame.math.Vector2(circle1.rect.center)
    distance = distance_vector.length()

    # Calculate the angle between the line connecting the circles and the x-axis
    angle = math.atan2(distance_vector.y, distance_vector.x)

    # Calculate the distance from the center of circle1 to the intersection point
    intersection_distance = (circle1.radius**2 - circle2.radius**2 + distance**2) / (2 * distance)

    # Calculate the coordinates of the intersection point
    intersection_x = circle1.rect.centerx + intersection_distance * math.cos(angle)
    intersection_y = circle1.rect.centery + intersection_distance * math.sin(angle)

    return intersection_x, intersection_y

def main():
    # Create a circle sprite in the middle of the screen
    circle_sprite = Circle(WIDTH // 2, HEIGHT // 2, 50, RED)
    
    circle_sprite_2 = Circle(WIDTH // 4, HEIGHT // 4, 50, RED)

    # Create a circle sprite for the mouse pointer
    mouse_circle_sprite = Circle(0, 0, 15, RED)

    # Create a blue circle sprite for collision indication
    blue_circle_sprite = Circle(0, 0, 15, BLUE)

    # Create sprite groups
    all_sprites = pygame.sprite.Group(circle_sprite, mouse_circle_sprite, blue_circle_sprite,circle_sprite_2)

    # Variable to track the duration of the collision indication
    collision_duration = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update the position of the mouse circle sprite
        mouse_circle_sprite.rect.center = (mouse_x, mouse_y)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the sprites
        all_sprites.draw(screen)

        # If there is a collision, calculate the intersection point and draw the blue circle at that point
        if pygame.sprite.collide_circle(circle_sprite, mouse_circle_sprite):
            intersection_point = find_intersection(circle_sprite, mouse_circle_sprite)
            blue_circle_sprite.rect.center = intersection_point
            collision_duration = 20  # Set the duration (in frames) for displaying the blue circle

            # Print the collision point coordinates
            print("Collision Point:", intersection_point)

        # Draw the blue circle for collision indication
        if collision_duration > 0:
            all_sprites.draw(screen)
            collision_duration -= 1

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
