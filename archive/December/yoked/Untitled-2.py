# %%
#test
a = 10

# %%
import pygame
import numpy as np
import sys

class Particle:
    def __init__(self, x, y, vx, vy, radius=50, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.base_color = color
        self.clicked = False  # Track whether the particle is clicked

    def overlaps(self, other):
        return np.hypot(self.x - other.x, self.y - other.y) < self.radius + other.radius

    def is_clicked(self, mouse_pos):
        return np.hypot(self.x - mouse_pos[0], self.y - mouse_pos[1]) < self.radius

    def draw(self, screen):
        darken_factor = 0.8 if self.clicked else 1.0
        darkened_color = tuple(int(c * darken_factor) for c in self.base_color)
        pygame.draw.circle(screen, darkened_color, (int(self.x), int(self.y)), self.radius)

    def advance(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Bounce off the walls
        if self.x - self.radius < 0 or self.x + self.radius > 800:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > 600:
            self.vy = -self.vy

    def handle_collision(self, other):
        """Handle a collision with another particle."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = np.hypot(dx, dy)

        if distance < self.radius + other.radius:
            angle = np.arctan2(dy, dx)
            overlap = (self.radius + other.radius - distance) * 0.5

            self.x -= overlap * np.cos(angle)
            self.y -= overlap * np.sin(angle)
            other.x += overlap * np.cos(angle)
            other.y += overlap * np.sin(angle)

            angle_collision = np.arctan2(other.y - self.y, other.x - self.x)
            magnitude_self = -(np.hypot(self.vx, self.vy))
            magnitude_other = -(np.hypot(other.vx, other.vy))

            new_vx_self = magnitude_other * np.cos(angle_collision)
            new_vy_self = magnitude_other * np.sin(angle_collision)
            new_vx_other = magnitude_self * np.cos(angle_collision + np.pi)
            new_vy_other = magnitude_self * np.sin(angle_collision + np.pi)

            self.vx, self.vy = new_vx_self, new_vy_self
            other.vx, other.vy = new_vx_other, new_vy_other

class Simulation:
    def __init__(self, n_particles):
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255)  # Magenta
        ]

        self.particles = []
        for i in range(n_particles):
            x = np.random.uniform(100, 600)
            y = np.random.uniform(100, 500)
            vx = np.random.uniform(-150, 150)
            vy = np.random.uniform(-150, 150)
            radius = 50
            color = self.colors[i % len(self.colors)]  # Cycle through colors
            self.particles.append(Particle(x, y, vx, vy, radius, color))

    def handle_collisions(self):
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.particles[i].overlaps(self.particles[j]):
                    self.particles[i].handle_collision(self.particles[j])
                    self.adjust_positions()

    def adjust_positions(self):
        for particle in self.particles:
            particle.advance(0.01)

    def darken_color_on_click(self, mouse_pos):
        for particle in self.particles:
            if particle.is_clicked(mouse_pos):
                particle.clicked = True
            else:
                particle.clicked = False

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for particle in self.particles:
                if particle.is_clicked(mouse_pos):
                    particle.clicked = not particle.clicked  # Toggle the clicked state

    def advance(self, dt, mouse_pos):
        self.handle_collisions()
        self.adjust_positions()
        # self.darken_color_on_click(mouse_pos)

    def run_simulation(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_mouse_events(event)

            screen.fill((255, 255, 255))

            self.advance(0.1, pygame.mouse.get_pos())  # Adjust the time step as needed

            for particle in self.particles:
                particle.draw(screen)

            pygame.display.flip()
            clock.tick(30)  # Adjust the frame rate as needed
# %%
if __name__ == "__main__":
    sim = Simulation(n_particles=5)
    sim.run_simulation()
