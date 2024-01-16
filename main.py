# %%
import logtocsv
# logtocsv.write_data(string)
# NOTE: Change over delay can be to or from given ball
import pygame
import sys
import os
import numpy as np
from ExperimentConfigWindow import ExperimentConfigWindow  # from ExperimentConfigWindow import ExperimentConfigWindow
import tkinter as tk
# from tkinter import filedialog

from time import strftime # see format codes: https://docs.python.org/3/library/datetime.html#format-codes

BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (185, 185, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
INDIGO = (75, 0, 130)
DARK_INDIGO = (54, 0, 94)
VIOLET = (128, 0, 128)
DARK_VIOLET = (80, 0, 80)
SQUARE_COLOR = (255, 255, 255)
SQUARE_THICKNESS = 4


phase_values=None
current_phase = 1
number_phases = 3
nparticles = 3
end_time = 0
# radius = 60
phase_time = 0
start_time = 0

values=None
base_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]  # Rainbow colors
clicked_colors = [DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN, DARK_BLUE, DARK_INDIGO, DARK_VIOLET]  # Darker shades of rainbow colors
radii = [60,60,60,60,60,60,60]
min_score_delay = [0.1,0.1,0.1,0.1,0.1,0.1,0.1] #min_score_delay = [0.1,0.1,0.1,0.1,0.1,0.1,0.1]  [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
change_over_delay = [2,2,2,2,2,2,2]
initial_speed_range = [(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1)]#(min,max)
speed_limits = [(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1) ]#(min,max)

fixed_interval = [1,1,1,1,1,1,1]
fixed_ratio = [1,1,1,1,1,1,1]
block_score_until = [0,0,0,0,0,0,0]

# Initialize Pygame
pygame.init()
# pygame.font.init()
font = pygame.font.Font(None, 36)  # Choose a font and size


experimentdate = strftime('%a %d %b %Y, %I:%M%p')
logtocsv.write_data(experimentdate)
print('experiment date:',experimentdate)

# Set up the window
os.environ["SDL_VIDEO_CENTERED"] = "1"
clock = pygame.time.Clock()
padding = 0
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
windowX, windowY = displayX - padding, displayY - padding # Here I was subtracging padding
screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window")

yoked = False
debug = False
# Set up the square
square_color = (255, 0, 0)
min_margin = 20
square_size = min(windowX, windowY) - 2 * min_margin
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)

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
total_score = 0
event = None
current_seconds = 0
#counters
clicked_on_particle = False

## This portion is key for our "Reverse lookup" dictionary
color_names = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "DARK_RED": (139, 0, 0),
    "ORANGE": (255, 165, 0),
    "DARK_ORANGE": (255, 140, 0),
    "YELLOW": (255, 255, 0),
    "DARK_YELLOW": (185, 185, 0),
    "GREEN": (0, 128, 0),
    "DARK_GREEN": (0, 100, 0),
    "BLUE": (0, 0, 255),
    "DARK_BLUE": (0, 0, 139),
    "INDIGO": (75, 0, 130),
    "DARK_INDIGO": (54, 0, 94),
    "VIOLET": (128, 0, 128),
    "DARK_VIOLET": (80, 0, 80),
    "SQUARE_COLOR": (255, 255, 255),
    "SQUARE_THICKNESS": 4,
}

reverse_lookup = {v: k for k, v in color_names.items()}

text_rect = None
# %%
class Particle:
    # particle = Particle(x, y, dx, dy, radius, color, particle_color,clicked_colors[i],min_score_delay,change_over_delay)
    def __init__(self, x, y, dx, dy, radius, base_color ,particle_color, clicked_color,min_score_delay,change_over_delay,block_score_until,fixed_interval,fixed_ratio):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.base_color = base_color or (0, 0, 255)
        self.clicked_color = clicked_color or (128, 128, 128)
        self.color = self.base_color
        self.colorname = particle_color
        self.clicked = False
        self.clicks = 0
        self.score = 0
        self.block_score_until = 0
        self.min_score_delay = min_score_delay
        self.change_over_delay = change_over_delay
        self.no_score_until = 0
        self.valid_clicks = 0 # set the amount of clicks to zero, so we can use the fixed ratio
        self.fixed_interval = fixed_interval
        self.fixed_ratio = fixed_ratio

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def advance(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x - self.radius < bounce_box_left:
            self.x = bounce_box_left + self.radius
            self.dx = abs(self.dx)
        elif self.x + self.radius > bounce_box_right:
            self.x = bounce_box_right - self.radius
            self.dx = -abs(self.dx)

        if self.y - self.radius < bounce_box_bottom:
            self.y = bounce_box_bottom + self.radius
            self.dy = abs(self.dy)
        elif self.y + self.radius > bounce_box_top:
            self.y = bounce_box_top - self.radius
            self.dy = -abs(self.dy)

    def darken_color(self):
        self.color = tuple(int(c * 0.8) for c in self.base_color)

    def lighten_color(self):
        self.color = self.base_color

# %%
class Simulation:
    def __init__(self, nparticles, radii): #def __init__(self, nparticles, radius=100, base_colors=None, clicked_colors=None):
        global base_colors, clicked_colors
        base_colors = base_colors  #base_colors = base_colors or [(0, 0, 255) for _ in range(nparticles)]
        clicked_colors = clicked_colors or [(128, 128, 128) for _ in range(nparticles)]
        self.particles = self.init_particles(nparticles, radii, base_colors, clicked_colors,min_score_delay,change_over_delay,block_score_until)

    def init_particles(self, nparticles, radii, base_colors, clicked_colors,min_score_delay,change_over_delay,block_score_until):
        logtocsv.write_data(('################# INIT particles ######################'))
        # global min_score_delay
        particles = []
        event_string = str(pygame.time.get_ticks()/1000) + ', Init stimuli, ' + str(total_score) + ', '

        for i in range(nparticles):
            radius = radii[i]
            # change_over_delay = change_over_delay[i]
            while True:
                x = np.random.uniform(radius, windowX - radii[i])
                y = np.random.uniform(radius, windowY - radii[i])
                dx = np.random.uniform(0.1, 0.12)
                dy = np.random.uniform(0.1, 0.12)
                color = base_colors[i]
                radius = radii[i]
                particle_color = reverse_lookup.get(color)
                particle = Particle(x, y, dx, dy, radius, color, particle_color,clicked_colors[i],min_score_delay[i],change_over_delay[i],block_score_until[i],fixed_interval[i],fixed_ratio[i])
                event_string += str(particle_color)+ ' x='+ str(int(particle.x)) + ' y='+ str(int(particle.y)) + ' dx='+ str((particle.dx))+ ' dy='+ str((particle.dy)) + ' clicks='+ str((particle.clicks))+ ' score='+ str((particle.score))+', '
                # print(event_string)
                overlaps = any(
                    np.hypot(particle.x - p.x, particle.y - p.y) < particle.radius + p.radius
                    or np.hypot(particle.x - p.x, particle.y - p.y) < p.radius - particle.radius
                    for p in particles
                )

                if not overlaps:
                    particles.append(particle)
                    break
                # event_string += str(particle_color)+ ' x='+ str(int(particle.x)) + ' y='+ str(int(particle.y)) + ' dx='+ str((particle.dx))+ ' dy='+ str((particle.dy)) + ' clicks='+ str((particle.clicks))+ ' score='+ str((particle.score))
                color = reverse_lookup.get(particle.base_color, "Unknown Color")
                event_string += ' ' + str(color) +':'
                event_string += ' x='+ str(int(particle.x)) +', '+ ' y='+ str(int(particle.y))+', ' + ' dx='+ str((particle.dx))+ ', '+' dy='+ str((particle.dy))  +', '+' clicks='+ str((particle.clicks))+', '+' score='+ str((particle.score))+','
                # 66.333, 0, Clicked ORANGE, x=370 y=540 RED x=688 y=431 dx=0.10210023218610983 dy=-0.11956539525490884 clicks=0 score=0 ORANGE x=355 y=557 dx=0.10852871091956233 dy=0.11269186047523638 clicks=1 score=0 YELLOW x=1177 y=538 dx=-0.11534114878188889 dy=-0.1124286037571398 clicks=0 score=0
                # print(event_string)
                for particle in particles:
                    color = reverse_lookup.get(particle.base_color, "Unknown Color")
                    event_string += ' ' + str(color) +':'
                    event_string += ' x='+ str(int(particle.x)) +', '+ ' y='+ str(int(particle.y))+', ' + ' dx='+ str((particle.dx))+ ', '+' dy='+ str((particle.dy))  +', '+' clicks='+ str((particle.clicks))+', '+' score='+ str((particle.score))+','
                    # 66.333, 0, Clicked ORANGE, x=370 y=540 RED x=688 y=431 dx=0.10210023218610983 dy=-0.11956539525490884 clicks=0 score=0 ORANGE x=355 y=557 dx=0.10852871091956233 dy=0.11269186047523638 clicks=1 score=0 YELLOW x=1177 y=538 dx=-0.11534114878188889 dy=-0.1124286037571398 clicks=0 score=0
                    # print('init particle',event_string)
        # print(event_string)
        for particle in particles:
            color = reverse_lookup.get(particle.base_color, "Unknown Color")
            event_string += ' ' + str(color) +':'
            event_string += ' x='+ str(int(particle.x)) +', '+ ' y='+ str(int(particle.y))+', ' + ' dx='+ str((particle.dx))+ ', '+' dy='+ str((particle.dy))  +', '+' clicks='+ str((particle.clicks))+', '+' score='+ str((particle.score))+','
            # 66.333, 0, Clicked ORANGE, x=370 y=540 RED x=688 y=431 dx=0.10210023218610983 dy=-0.11956539525490884 clicks=0 score=0 ORANGE x=355 y=557 dx=0.10852871091956233 dy=0.11269186047523638 clicks=1 score=0 YELLOW x=1177 y=538 dx=-0.11534114878188889 dy=-0.1124286037571398 clicks=0 score=0
        logtocsv.write_data(event_string)    
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
        v1, v2 = np.array([p1.dx, p1.dy]), np.array([p2.dx, p2.dy])
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.dx, p1.dy = u1
        p2.dx, p2.dy = u2

    def advance(self, dt):
        for particle in self.particles:
            particle.advance(dt)
        self.handle_collisions()
# %%
def main():
    global screen, windowX, windowY, bounce_box_right, bounce_box_top, square_rect, font, current_phase, number_phases, text_rect, current_seconds,clicked_on_particle, total_score, phase_time, end_time, phase_values
    logtocsv.write_data(('################# Phase '+str(current_phase)+' ######################'))
    clock = pygame.time.Clock()
    sim = Simulation(nparticles, radii)

    shuffle_button_rect = pygame.Rect(windowX - 150, 20, 120, 30)
    shuffle_button_color = (255, 100, 100)

    total_score = 0

    # while True:
    print(current_seconds)
    while current_seconds < end_time:
        # Handle events here
        current_seconds = pygame.time.get_ticks()/1000 - start_time
        # print(current_seconds)
        for event in pygame.event.get():
            event_string = str(current_seconds)+', ' + str(total_score) + ', '# start making my string
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # logtocsv.write_data(str(current_seconds)+' Testing doing a random string')
                    
                    for particle in sim.particles:
                        # if current_seconds > particle.block_score_until:
                        #     break
                        if np.hypot(event.pos[0] - particle.x, event.pos[1] - particle.y) < particle.radius:
                            # Handle the clicked particle

                            # particle.block_score_until = current_seconds + particle.min_score_delay
                            clicked_on_particle = True
                            particle.darken_color()
                            particle.clicked = True
                            particle.clicks += 1
                            clicked_color = particle.colorname
                            event_string += "Clicked: "+clicked_color +', '
                            event_string += 'x='+ str(event.pos[0])+', ' + ' y='+ str(event.pos[1])+', '
                            if current_seconds < particle.block_score_until:
                                print('clicked:',particle.colorname,current_seconds , "can't score now, score blocked by time", end='')
                                for particle in sim.particles:
                                    print(particle.block_score_until, end=' ,')
                                print('')
                                break
                            elif current_seconds >= particle.block_score_until:
                                print('scored at',current_seconds,'Was blocked until: ',particle.block_score_until)
                                particle.score += 1
                                total_score +=1
                                particle.block_score_until = current_seconds + particle.min_score_delay
                                for particle in sim.particles:
                                    if np.hypot(event.pos[0] - particle.x, event.pos[1] - particle.y) < particle.radius:
                                        pass
                                    else:
                                        particle.block_score_until = current_seconds + particle.change_over_delay

                            # Handle.clicked_stimuli(clicked_color,event.pos[0],event.pos[1])
                            # else:
                            #     # Handle particles that were not clicked
                            #     # print('Else')
                            #     particle.block_score_until = current_seconds + particle.change_over_delay

                                # particle.block_score_until= current_seconds + particle.change_over_delay

                if not clicked_on_particle and not shuffle_button_rect.collidepoint(event.pos):
                    event_string += 'Clicked: None, '
                    event_string += f'x={event.pos[0]}, y={event.pos[1]}, '

                clicked_on_particle = False
                if shuffle_button_rect.collidepoint(event.pos):
                    # Check if the shuffle button is clicked
                    sim = Simulation(nparticles, radii)  # Create a new simulation to reorient all balls
                    event_string += 'Clicked: Shuffle, '
                    event_string += f'x={event.pos[0]}, y={event.pos[1]}, '
                    # print('Clicked: Shuffle')

                for particle in sim.particles:
                    color = reverse_lookup.get(particle.base_color, "Unknown Color")
                    event_string += ' ' + str(color) +':'
                    event_string += ' x='+ str(int(particle.x)) +', '+ ' y='+ str(int(particle.y))+', ' + ' dx='+ str((particle.dx))+ ', '+' dy='+ str((particle.dy))  +', '+' clicks='+ str((particle.clicks))+', '+' score='+ str((particle.score))+','
                    # 66.333, 0, Clicked ORANGE, x=370 y=540 RED x=688 y=431 dx=0.10210023218610983 dy=-0.11956539525490884 clicks=0 score=0 ORANGE x=355 y=557 dx=0.10852871091956233 dy=0.11269186047523638 clicks=1 score=0 YELLOW x=1177 y=538 dx=-0.11534114878188889 dy=-0.1124286037571398 clicks=0 score=0
                    # print(event_string)

                logtocsv.write_data(event_string)

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
        text_score = font.render(f'Score: {total_score}', True, YELLOW)
        text_rect_score = text_score.get_rect(center=(windowX // 2, windowY - 60))
        screen.blit(text_score, text_rect_score)
        # screen.blit(text_ball_2, text_rect_ball_2)
        
        font = pygame.font.Font(None, 36)
        text = font.render("Shuffle", True, (255, 255, 255))
        screen.blit(text, (windowX - 140, 25))
        pygame.display.flip()
        clock.tick(60)
    current_phase += 1
    print('Current time',current_seconds,'end tiime',end_time)
    if current_phase <= number_phases:
        print('Current Phase',current_phase,'Number of Phases',number_phases,'Current time',current_seconds,'end time:',end_time,'Phase time:',phase_time)
        phase_time = phase_values[current_phase-1]['duration_of_phase'] # GET all values like thisvalues[0]['number_phases'] # GET all values like this values[current_phase-1]['phase_time'] # GET all values like this
        print('phase tiime',phase_time)
        end_time += int(phase_time)
        clock = pygame.time.Clock()
        main()
# %%
if __name__ == "__main__":
    root_main = tk.Tk()
    def callback(values):
        global phase_time, number_phases, phase_values,end_time, clock,start_time
        print('In callback function')
        number_phases=values[0]['number_phases']
        # print(phase_values)
        phase_values = values
        phase_time = phase_values[current_phase-1]['duration_of_phase'] # GET all values like thisvalues[0]['number_phases'] # GET all values like this values[current_phase-1]['phase_time'] # GET all values like this
        end_time += int(phase_time) #end_time += pygame.time.get_ticks()/1000+int(phase_time)
        print('end time',end_time)
        clock = pygame.time.Clock()  # Reset the clock
        # current_seconds = pygame.time.get_ticks() / 1000 ## current_seconds = pygame.time.Clock.get_time()    #
        config_window.root.destroy()
        # phase_values[0]['participant_id'] # GET all values like this
        start_time = pygame.time.get_ticks()/1000
    
    # Create an instance of the ExperimentConfigWindow class
    config_window = ExperimentConfigWindow(root_main)
    config_window.callback = callback  # Set the callback attribute

    # Start the Tkinter event loop
    root_main.mainloop()
    main()

# %%
