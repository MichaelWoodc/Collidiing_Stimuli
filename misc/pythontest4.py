import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Function to calculate distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Function to calculate angle between two points
def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

# Function to calculate force components
def calculate_force_components(speed, angle):
    force_x = speed * math.cos(angle)
    force_y = speed * math.sin(angle)
    return force_x, force_y

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collision Simulation")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Ball properties
ball_radius = BALL_RADIUS
ball1_pos = [100, 300]  # Starting position of the moving ball
ball1_speed = 5  # Initial speed of the moving ball
ball1_angle = math.radians(3)  # Initial angle in radians

ball2_pos = [500, 300]  # Starting position of the stationary ball
ball2_speed = 0  # Initial speed of the stationary ball

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Update ball positions
    ball1_pos[0] += ball1_speed * math.cos(ball1_angle)
    ball1_pos[1] += ball1_speed * math.sin(ball1_angle)

    # Check for collision
    if distance(ball1_pos[0], ball1_pos[1], ball2_pos[0], ball2_pos[1]) <= 2 * ball_radius:
        # Collision detected
        collision_angle = calculate_angle(ball1_pos[0], ball1_pos[1], ball2_pos[0], ball2_pos[1])
        print(f"Collision Angle: {math.degrees(collision_angle)} degrees")

        # Calculate force components for both balls
        force1_x, force1_y = calculate_force_components(ball1_speed, collision_angle)
        force2_x, force2_y = calculate_force_components(ball2_speed, collision_angle)

        # Update velocities of the balls (conservation of momentum)
        ball1_speed_after = ball1_speed
        ball2_speed_after = ball2_speed

        # Update positions of the balls
        ball1_pos[0] += ball1_speed_after * math.cos(collision_angle)
        ball1_pos[1] += ball1_speed_after * math.sin(collision_angle)

        ball2_pos[0] += ball2_speed_after * math.cos(collision_angle)
        ball2_pos[1] += ball2_speed_after * math.sin(collision_angle)

        # Stop animation
        running = False

    # Draw balls
    pygame.draw.circle(screen, RED, (int(ball1_pos[0]), int(ball1_pos[1])), ball_radius)
    pygame.draw.circle(screen, RED, (int(ball2_pos[0]), int(ball2_pos[1])), ball_radius)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

# Wait for user input before simulating post-collision path
input("Press Enter to simulate post-collision path...")

# Simulate post-collision path
post_collision_speed1 = ball1_speed_after
post_collision_speed2 = ball2_speed_after

# Main loop for post-collision simulation
while ball1_pos[0] > ball_radius or ball2_pos[0] < WIDTH - ball_radius:
    screen.fill(WHITE)

    # Update ball positions
    ball1_pos[0] += post_collision_speed1 * math.cos(collision_angle)
    ball1_pos[1] += post_collision_speed1 * math.sin(collision_angle)

    ball2_pos[0] += post_collision_speed2 * math.cos(collision_angle)
    ball2_pos[1] += post_collision_speed2 * math.sin(collision_angle)

    # Draw balls
    pygame.draw.circle(screen, RED, (int(ball1_pos[0]), int(ball1_pos[1])), ball_radius)
    pygame.draw.circle(screen, RED, (int(ball2_pos[0]), int(ball2_pos[1])), ball_radius)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
