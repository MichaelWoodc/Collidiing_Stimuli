# %%
import pygame
import sys
import os
import numpy as np
# import csv
from time import strftime # see format codes: https://docs.python.org/3/library/datetime.html#format-codes

## https://pythonexamples.org/python-print-to-file/#:~:text=Print%20to%20File%20in%20Python%201%20Open%20file,%28%29%20statement%20shall%20be%20written%20to%20the%20file.
# f = open('my_log.txt', 'a')
# The syntax to print a string to the file is

# print("Hello World", file=f)
  
# Initialize Pygame
pygame.init()
# pygame.font.init()
font = pygame.font.Font(None, 36)  # Choose a font and size

experimentdate = strftime('%a %d %b %Y, %I:%M%p')
print('experiment date:',experimentdate)
filedate = strftime('%Y_%m_%d_%I_%M%p')
f = open(filedate+'.txt', 'a')
print('filedate',filedate)
# print("Clicked in empty location:",event.pos[0], event.pos[1], file=f) 
print('Time,','Event,','clicks_blue,','score_blue,','clicks_yellow,','score_yellow,','event_x,','event_y,','blue_x','blue_y','blue_dx','blue_dy','yellow_x','yellow_y','yellow_dx','yellow_dy',file=f) 
# # Specify the subfolder name
# subfolder = "reports"
# if not os.path.exists(subfolder):
#     os.makedirs(subfolder)
# file_path = os.path.join(subfolder, filedate + '.txt')  
# with open(file_path, 'a') as f:
#     # Your code for writing to the file goes here
#     # For example:
#     f.write("Hello, this is a sample content.")

# Set up the window
os.environ["SDL_VIDEO_CENTERED"] = "1"
clock = pygame.time.Clock()
padding = 100
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
windowX, windowY = displayX - 100, displayY - 100
screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window")

# Set up the square
square_color = (255, 0, 0)
min_margin = 20
square_size = min(windowX, windowY) - 2 * min_margin
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 255, 0)
SQUARE_COLOR = (255, 255, 255)
SQUARE_THICKNESS = 4


nparticles = 2
radius = 60
base_colors = [YELLOW, BLUE]  # Example colors
clicked_colors = [DARK_YELLOW, DARK_BLUE]  # Example clicked colors

margin = 100
margin_left = margin
margin_right = margin
margin_top = margin
margin_bottom = margin

bounce_box_left = margin_left
bounce_box_right = windowX - margin_right
bounce_box_top = windowY - margin_top
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)
bounce_box_bottom = margin_bottom

#Random variables for right here:
change_over_delay_between_balls = 3
score_delay = 0.5 # seconds between scoring events per given ball.  affects scoring in all cases
event = None
current_seconds = 0
#counters
click_count_blue = 0
click_count_yellow = 0
score_count_blue = 0
score_count_yellow = 0
last_click_blue = 0
last_click_yellow = 0
last_score_blue = -change_over_delay_between_balls
last_score_yellow = -change_over_delay_between_balls

## This portion is key for our "Reverse lookup" dictionary
color_names = {
    "BLACK": (0, 0, 0),
    "BLUE": (0, 0, 255),
    "DARK_BLUE": (0, 0, 200),
    "YELLOW": (255, 255, 0),
    "DARK_YELLOW": (200, 255, 0),
}
reverse_lookup = {v: k for k, v in color_names.items()}

text_rect = None

# %%
class HandleClicks:
    def handleScoring(clicked_color):
        global last_score_blue, last_score_yellow


    def handle_clicked_stimuli(clicked_color,event_x,event_y):
        global click_count_blue, score_count_blue, last_click_blue, last_score_blue, click_count_yellow, score_count_yellow,  last_click_yellow, last_score_yellow
        
        
        if clicked_color == 'BLUE':
            click_count_blue += 1
            last_click_blue = current_seconds
            if last_click_blue >= last_score_yellow + (change_over_delay_between_balls):
                print(f"{clicked_color}Score:",score_count_blue,'at time',current_seconds,'seconds',file=f) #print(f"{clicked_color}Score:",score_count_blue,'at time',current_seconds,'seconds',file=f)
                print('BLUE') #for event in pygame.event.get():print("Clicked in empty location:",event.pos[0], event.pos[1], file=f) print("Clicked nothing", file=f)
                score_count_blue += 1
                last_score_blue = last_click_blue
            else:
                print(f"Clicked Stimuli: {clicked_color}","at",current_seconds,'seconds')
                #print('Too soon to score!')
        elif clicked_color == 'YELLOW':
            click_count_yellow += 1
            last_click_yellow = current_seconds
            if last_click_yellow >= last_score_blue + change_over_delay_between_balls:
                score_count_yellow+=1
                last_score_yellow = last_click_yellow
        else:
            print('Clicked a random spot')
            # print("Clicked nothing", file=f)


# %%
class Particle:
    def __init__(self, x, y, vx, vy, radius=10, base_color=None, clicked_color=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.base_color = base_color or (0, 0, 255)
        self.clicked_color = clicked_color or (128, 128, 128)
        self.color = self.base_color
        self.clicked = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def advance(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x - self.radius < bounce_box_left:
            self.x = bounce_box_left + self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > bounce_box_right:
            self.x = bounce_box_right - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius < bounce_box_bottom:
            self.y = bounce_box_bottom + self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > bounce_box_top:
            self.y = bounce_box_top - self.radius
            self.vy = -abs(self.vy)

    def darken_color(self):
        self.color = tuple(int(c * 0.8) for c in self.base_color)

    def lighten_color(self):
        self.color = self.base_color

# %%
class Simulation:
    def __init__(self, nparticles, radius=100): #def __init__(self, nparticles, radius=100, base_colors=None, clicked_colors=None):
        global base_colors, clicked_colors
        base_colors = base_colors  #base_colors = base_colors or [(0, 0, 255) for _ in range(nparticles)]
        clicked_colors = clicked_colors or [(128, 128, 128) for _ in range(nparticles)]
        self.particles = self.init_particles(nparticles, radius, base_colors, clicked_colors)

    def init_particles(self, nparticles, radius, base_colors, clicked_colors):
        particles = []
        for i in range(nparticles):
            while True:
                x = np.random.uniform(radius, windowX - radius)
                y = np.random.uniform(radius, windowY - radius)
                vx = np.random.uniform(0.1, 0.12)   #vx = np.random.uniform(-0.1, 0.1)
                vy = np.random.uniform(0.1, 0.12)   #vy = np.random.uniform(-0.1, 0.1)
                color = base_colors[i]

                particle = Particle(x, y, vx, vy, radius, color, clicked_colors[i])

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
            for j in range(i + 1, len(self.particles)):
                if np.hypot(self.particles[i].x - self.particles[j].x,
                            self.particles[i].y - self.particles[j].y) < self.particles[i].radius + self.particles[
                    j].radius:
                    self.change_velocities(self.particles[i], self.particles[j])

    def change_velocities(self, p1, p2):
        m1, m2 = p1.radius ** 2, p2.radius ** 2
        M = m1 + m2
        r1, r2 = np.array([p1.x, p1.y]), np.array([p2.x, p2.y])
        d = np.linalg.norm(r1 - r2) ** 2
        v1, v2 = np.array([p1.vx, p1.vy]), np.array([p2.vx, p2.vy])
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.vx, p1.vy = u1
        p2.vx, p2.vy = u2

    def advance(self, dt):
        for particle in self.particles:
            particle.advance(dt)
        self.handle_collisions()
# %%
def main():
    global screen, windowX, windowY, bounce_box_right, bounce_box_top, square_rect, font, last_score_blue,change_over_delay_between_balls,last_score_yellow, text_rect, current_seconds
    
    clock = pygame.time.Clock()
    sim = Simulation(nparticles, radius)



    

    shuffle_button_rect = pygame.Rect(windowX - 150, 20, 120, 30)
    shuffle_button_color = (255, 100, 100)

    while True:
        # Handle events here
        current_seconds = pygame.time.get_ticks()/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for particle in sim.particles:
                        if np.hypot(event.pos[0] - particle.x, event.pos[1] - particle.y) < particle.radius:
                            # print('This particle',particle)
                            particle.darken_color()
                            particle.clicked = True
                            clicked_color = reverse_lookup.get(particle.base_color, "Unknown Color")
                            # print(f"Clicked Particle Color: {clicked_color}","at",current_seconds,'seconds')
                            # if clicked_color == 'BLUE':
                            #     click_count_blue += 1
                            HandleClicks.handle_clicked_stimuli(clicked_color,event.pos[0],event.pos[1])
                            #     last_click_blue = current_seconds
                            # elif clicked_color == 'YELLOW':
                            #     click_count_yellow += 1
                            #     last_click_yellow = current_seconds
                        else:
                            print("Clicked in empty location:",event.pos[0], event.pos[1], file=f)    
                # Inside the main function
                if shuffle_button_rect.collidepoint(event.pos):
                    # Check if the shuffle button is clicked
                    sim = Simulation(nparticles, radius)  # Create a new simulation to reorient all balls
                    print('Clicked shuffle')

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for particle in sim.particles:
                        if particle.clicked:
                            particle.lighten_color()
                            particle.clicked = False
            elif event.type == pygame.VIDEORESIZE:
                windowX, windowY = event.w, event.h
                screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                bounce_box_right = windowX - margin_right
                bounce_box_top = windowY - margin_top
                square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size,
                                          square_size)
        
        screen.fill((0, 0, 0))

        sim.advance(20.0)

        for particle in sim.particles:
            particle.draw(screen)

        pygame.draw.rect(screen, SQUARE_COLOR, (margin, margin, windowX - 2 * (margin), windowY - 2 * (margin)),
                         SQUARE_THICKNESS)

        # Draw the shuffle button
        pygame.draw.rect(screen, shuffle_button_color, shuffle_button_rect)
        text_ball_1 = font.render(f'Blue Clicks: {click_count_blue} Blue score {score_count_blue}', True, BLUE)
        text_ball_2 = font.render(f'Yellow Clicks: {click_count_yellow} Yellow score {score_count_yellow}', True, YELLOW)
        text_rect_ball_1 = text_ball_1.get_rect(center=(windowX // 2, windowY - 60))
        text_rect_ball_2 = text_ball_2.get_rect(center=(windowX // 2, windowY - 30))
        # print((current_seconds-last_score_blue+change_over_delay_between_balls))
        test = round(
            max(
            ((last_score_blue + change_over_delay_between_balls)-current_seconds),
            ((last_score_yellow + change_over_delay_between_balls)-current_seconds)),
            2)
        # print('test',test)
        if test >=0:
            text_change_over_delay = font.render(f'Change over delay timer: {test}', True, YELLOW)
            if text_rect == None:
                text_rect = text_change_over_delay.get_rect(center=(windowX // 2, windowY - 10))
            screen.blit(text_change_over_delay, text_rect)
        screen.blit(text_ball_1, text_rect_ball_1)
        screen.blit(text_ball_2, text_rect_ball_2)
        
        font = pygame.font.Font(None, 36)
        text = font.render("Shuffle", True, (255, 255, 255))
        screen.blit(text, (windowX - 140, 25))

        pygame.display.flip()
        clock.tick(60)
# %%
if __name__ == '__main__':
    main()

# %%
