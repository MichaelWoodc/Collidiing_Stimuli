import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create an initial window
width, height = 400, 400
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("TEST")

stimuli = {'ball1': {'color': BLUE, 'radius': 10, 'x': 100, 'y': 200, 'dx': 6, 'dy': 0},
           'ball2': {'color': RED, 'radius': 10, 'x': 20, 'y': 200, 'dx': 1, 'dy': 0}}

def bounce():
    global stimuli
    for key in stimuli.keys():
        x, y = stimuli[key]['x'], stimuli[key]['y']

        if x - stimuli[key]['radius'] <= 0 or x + stimuli[key]['radius'] >= width:
            stimuli[key]['dx'] = -stimuli[key]['dx']

        if y - stimuli[key]['radius'] <= 0 or y + stimuli[key]['radius'] >= height:
            stimuli[key]['dy'] = -stimuli[key]['dy']

def drawToDisplaySize():
    global width, height
    width, height = event.w, event.h

def drawStimuli():
    for key in stimuli.keys():
        drawThis = stimuli[key]
        pygame.draw.circle(
            screen,
            drawThis['color'],
            (stimuli[key]['x'], stimuli[key]['y']),
            drawThis['radius'],
        )

def moveStimuli():
    global stimuli
    for key in stimuli.keys():
        stimuli[key]['x'] += stimuli[key]['dx'] / 100
        stimuli[key]['y'] += stimuli[key]['dy'] / 100

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def elastic_collision(v1x, v1y, v2x, v2y, collision_point, angle1, angle2):
    # Calculate relative angles
    angle1_rel = math.atan2(v1y, v1x)
    angle2_rel = math.atan2(v2y, v2x)

    # Calculate the angle of collision
    collision_angle = math.atan2(collision_point[1] - collision_point[0], collision_point[0] - collision_point[0])

    # Calculate the relative velocities
    v1_rel = math.sqrt(v1x ** 2 + v1y ** 2)
    v2_rel = math.sqrt(v2x ** 2 + v2y ** 2)

    # Calculate the final velocities in the rotated coordinate system
    v1fx_rel = (v1_rel * math.cos(angle1_rel - collision_angle) * (1 - 1) + 2 * v2_rel * math.cos(angle2_rel - collision_angle)) / (1 + 1)
    v2fx_rel = (v2_rel * math.cos(angle2_rel - collision_angle) * (1 - 1) + 2 * v1_rel * math.cos(angle1_rel - collision_angle)) / (1 + 1)

    # Calculate the final velocities in the original coordinate system
    v1fx = v1fx_rel * math.cos(collision_angle) - v1_rel * math.sin(angle1_rel - collision_angle)
    v1fy = v1fx_rel * math.sin(collision_angle) + v1_rel * math.cos(angle1_rel - collision_angle)

    v2fx = v2fx_rel * math.cos(collision_angle) - v2_rel * math.sin(angle2_rel - collision_angle)
    v2fy = v2fx_rel * math.sin(collision_angle) + v2_rel * math.cos(angle2_rel - collision_angle)

    return v1fx, v1fy, v2fx, v2fy

def checkDistances():
    global stimuli
    for key in stimuli.keys():
        thisRadius = stimuli[key]['radius']
        thisX = stimuli[key]['x']
        thisY = stimuli[key]['y']
        for subkey in stimuli.keys():
            if subkey != key:
                otherX = stimuli[subkey]['x']
                otherY = stimuli[subkey]['y']
                otherRadius = stimuli[key]['radius']
                distance = calculate_distance(thisX, thisY, otherX, otherY)
                if distance <= thisRadius + otherRadius:
                    collide(key, subkey, (thisX, thisY), (otherX, otherY))

def collide(stim1, stim2, collision_point1, collision_point2):
    global stimuli
    angle1 = math.atan2(stimuli[stim1]['dy'], stimuli[stim1]['dx'])
    angle2 = math.atan2(stimuli[stim2]['dy'], stimuli[stim2]['dx'])
    stimuli[stim1]['dx'], stimuli[stim1]['dy'], stimuli[stim2]['dx'], stimuli[stim2]['dy'] = elastic_collision(
        stimuli[stim1]['dx'], stimuli[stim1]['dy'], stimuli[stim2]['dx'], stimuli[stim2]['dy'],
        collision_point1, angle1, angle2
    )
    moveStimuli()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            drawToDisplaySize()

    screen.fill(WHITE)
    moveStimuli()
    drawStimuli()
    bounce()
    checkDistances()
    pygame.display.flip()
