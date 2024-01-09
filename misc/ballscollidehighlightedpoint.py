import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 60
FPS = 60
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Ball class
class Ball:
    def __init__(self, color):
        self.radius = BALL_RADIUS
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.dx = random.choice([1, -1]) * random.randint(2, 5)
        self.dy = random.choice([1, -1]) * random.randint(2, 5)
        self.color = color

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx = -self.dx
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy = -self.dy

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.radius + other.radius:
            angle = math.atan2(dy, dx)

            # Calculate relative velocity
            dvx = self.dx - other.dx
            dvy = self.dy - other.dy

            # Calculate normal and tangent components of relative velocity
            normal_velocity = dvx * math.cos(angle) + dvy * math.sin(angle)
            tangent_velocity = -dvx * math.sin(angle) + dvy * math.cos(angle)

            # Calculate new normal velocities using 1D elastic collision formula
            new_normal_velocity_self = (
                (self.radius - other.radius) * normal_velocity +
                2 * other.radius * other.radius * normal_velocity
            ) / (self.radius + other.radius)

            new_normal_velocity_other = (
                (other.radius - self.radius) * normal_velocity +
                2 * self.radius * self.radius * normal_velocity
            ) / (self.radius + other.radius)

            # Update velocities
            self.dx = (new_normal_velocity_self * math.cos(angle) + tangent_velocity * math.cos(angle + math.pi / 2))/100
            self.dy = (new_normal_velocity_self * math.sin(angle) + tangent_velocity * math.sin(angle + math.pi / 2))/100

            other.dx = new_normal_velocity_other * math.cos(angle) + tangent_velocity * math.cos(angle + math.pi / 2)
            other.dy = new_normal_velocity_other * math.sin(angle) + tangent_velocity * math.sin(angle + math.pi / 2)

            # Highlight collision point
            collision_point = (
                int((self.x + other.x) / 2),
                int((self.y + other.y) / 2)
            )
            pygame.draw.circle(screen, RED, collision_point, 5)
            pygame.display.flip()
            # Print relative angle
            print("Relative Angle (Self): {:.2f} degrees".format(math.degrees(angle)))
            print("Relative Angle (Other): {:.2f} degrees".format(math.degrees(angle + math.pi)))

            # Pause the program on collision
            # pygame.time.wait(5)  # Pause for 2 seconds
            # sys.exit()  # Terminate the program

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Main loop
def main():
    blue_ball = Ball(BLUE)
    yellow_ball = Ball(YELLOW)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move balls
        blue_ball.move()
        yellow_ball.move()

        # Check for collisions
        blue_ball.collide(yellow_ball)

        # Clear the screen
        screen.fill(WHITE)

        # Draw balls
        blue_ball.draw()
        yellow_ball.draw()

        # Display instructions
        instructions_text = font.render("Program Paused on Collision. Exiting in 2 seconds...", True, (0, 0, 0))
        screen.blit(instructions_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
