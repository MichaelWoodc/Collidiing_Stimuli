import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Circles")

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Circle class
class Circle(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def update(self):
        # Move the circle
        self.rect.x += self.dx
        self.rect.y += self.dy

# Create circles based on stimuli
stimuli = {'ball1': {'color': blue, 'radius': 10, 'dx': 5, 'dy': 5},
           'ball2': {'color': red, 'radius': 10, 'dx': 4, 'dy': 2}}

circle1 = Circle(**stimuli['ball1'], x=200, y=300)
circle2 = Circle(**stimuli['ball2'], x=400, y=300)

# Create sprite groups
all_sprites = pygame.sprite.Group(circle1, circle2)

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update sprite group
    all_sprites.update()

    # Draw background
    screen.fill(white)

    # Draw sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
