import pygame
import numpy as np
import sys

class Particle:
    def __init__(self, x, y, vx, vy, radius=10, color=(0, 0, 255), margin=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.base_color = color  # Base color of the particle
        self.color = color  # Current color of the particle
        self.clicked = False  # Flag to track if the particle is clicked
        self.margin = margin  # Margin for the white square

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def advance(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Bound the particle inside the white square
        if self.x - self.radius < self.margin:
            self.x = self.radius + self.margin
            self.vx = abs(self.vx)  # Reflect velocity
        elif self.x + self.radius > 800 - self.margin:
            self.x = 800 - self.radius - self.margin
            self.vx = -abs(self.vx)  # Reflect velocity

        if self.y - self.radius < self.margin:
            self.y = self.radius + self.margin
            self.vy = abs(self.vy)  # Reflect velocity
        elif self.y + self.radius > 600 - self.margin:
            self.y = 600 - self.radius - self.margin
            self.vy = -abs(self.vy)  # Reflect velocity

    def darken_color(self):
        # Darken the color by multiplying each RGB component by 0.8
        self.color = tuple(int(c * 0.8) for c in self.base_color)

    def lighten_color(self):
        # Restore the original color
        self.color = self.base_color


class Simulation:
    def __init__(self, nparticles, radius=10, margin=20, left_image_path=None, right_image_path=None):
        self.particles = self.init_particles(nparticles, radius, margin)
        self.margin = margin

        # Load images if provided
        self.left_image = pygame.image.load(left_image_path) if left_image_path else None
        self.right_image = pygame.image.load(right_image_path) if right_image_path else None

    def init_particles(self, nparticles, radius, margin):
        particles = []
        for _ in range(nparticles):
            while True:
                x = np.random.uniform(radius + margin, 800 - radius - margin)
                y = np.random.uniform(radius + margin, 600 - radius - margin)
                vx = np.random.uniform(-0.1, 0.1)
                vy = np.random.uniform(-0.1, 0.1)
                color = tuple(np.random.randint(0, 256, 3))  # Random RGB color

                particle = Particle(x, y, vx, vy, radius, color, margin)

                # Check for overlaps with existing particles
                overlaps = any(
                    np.hypot(particle.x - p.x, particle.y - p.y) < particle.radius + p.radius
                    for p in particles
                )

                if not overlaps:
                    particles.append(particle)
                    break

        return particles

    def handle_collisions(self):
        for i in range(len(self.particles)):
            for j in range(i+1, len(self.particles)):
                if np.hypot(self.particles[i].x - self.particles[j].x,
                            self.particles[i].y - self.particles[j].y) < self.particles[i].radius + self.particles[j].radius:
                    self.change_velocities(self.particles[i], self.particles[j])

    def change_velocities(self, p1, p2):
        m1, m2 = p1.radius**2, p2.radius**2
        M = m1 + m2
        r1, r2 = np.array([p1.x, p1.y]), np.array([p2.x, p2.y])
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = np.array([p1.vx, p1.vy]), np.array([p2.vx, p2.vy])
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.vx, p1.vy = u1
        p2.vx, p2.vy = u2

    def advance(self, dt):
        for particle in self.particles:
            particle.advance(dt)
        self.handle_collisions()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    nparticles = 5
    radius = 60
    margin = 20
    left_image_path = "test.png"  # Specify the path to your left image
    right_image_path = "test.png"  # Specify the path to your right image

    sim = Simulation(nparticles, radius, margin, left_image_path, right_image_path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    for particle in sim.particles:
                        if np.hypot(event.pos[0] - particle.x, event.pos[1] - particle.y) < particle.radius:
                            particle.darken_color()
                            particle.clicked = True
                            print(f"Clicked Particle Color: {particle.base_color}")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    for particle in sim.particles:
                        if particle.clicked:
                            particle.lighten_color()
                            particle.clicked = False

        screen.fill((255, 255, 255))  # White background

        # Draw left and right images
        if sim.left_image:
            screen.blit(sim.left_image, (0, 0))
        if sim.right_image:
            screen.blit(sim.right_image, (400, 0))

        sim.advance(20.0)

        for particle in sim.particles:
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
