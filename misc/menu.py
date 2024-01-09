import pygame
import pygame_menu
import time
import csv
import os

from typing import Tuple


# expInfo = {}
# expInfo['date'] = time.strftime(("%Y_%m_%d-%H_%M"))
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.font.init() # you have to call this at the start if you want to use the module
clock = pygame.time.Clock()
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)# (displayX-10, displayY-10),pygame.RESIZABLE,display=0)
surfaceRectangle = surface.get_rect()

## Let's set up everything for the text
font1 = pygame.font.Font(pygame.font.match_font('sans'), 50)
font2 = pygame.font.Font(pygame.font.match_font('sans.bold'), 70)
my_font = pygame.font.Font('freesansbold.ttf', 55)
# fontslist=[font1,font1,font1,font1,font1]
black = (0,0,0)
textTopPadding = 200
menuPadding = 100 # value in pixels
background_color = (200,200,200)


### Boolean Values go here ###  TODO: move all boolean values here
displayMainMenu = True

def testConditions(testIndex):
    global dictIndex, file, danvasubtest
    if testIndex == 0:
        file = ('src/stimFiles/'+ 'adultFaces.csv')
        danvasubtest = 'Adult Faces'
    if testIndex == 1:
        file = ('src/stimFiles/'+ 'adultPostures.csv')
        danvasubtest = 'Adult Postures'
    if testIndex == 2:
        file = ('src/stimFiles/'+ 'childFaces.csv')
        danvasubtest = 'Child Faces'
    if testIndex == 3:
        file = ('src/stimFiles/'+ 'adultVoices.csv')
        danvasubtest = 'Adult Voices'
    if testIndex == 4:
        file = ('src/stimFiles/'+ 'childVoices.csv')
        danvasubtest = 'Child Voices'


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
    
def displayUpdate(clear = 0):
    global events
    if clear == 0:
        # events = pygame.event.get()
        pygame.display.update()
    else:
        surface.fill((background_color))
        pygame.display.update()
    

def mainMenuState():#(state)
    global displayMainMenu, showInstructions
    # displayMainMenu = False
    showInstructions = True
    # displayInstructions()

width, height = surface.get_size()

menu = pygame_menu.Menu('Welcome to the DANVA II test, please enter your information below', width - menuPadding, height - menuPadding,
                    theme=pygame_menu.themes.THEME_BLUE)

sessionInput = menu.add.text_input('Session :  ', default='001')
session= sessionInput.get_value()
participantInput = menu.add.text_input('Participant :  ', default='')
participant = participantInput.get_value() # put this in the pdf function
ageInput = menu.add.text_input('Age :    ', default='')
age = ageInput.get_value()

def printSelected (value: Tuple[str,int], index = str):
    print(index)
    global file, dictIndex
    test = (value[0])
    testIndex = (test[1])
    dictIndex = 0
    testConditions(testIndex)

testSelector = menu.add.dropselect(
    onchange=(printSelected),
    title='Select Test',
    items=[('Adult Faces', 0),
        ('Adult Postures', 1),
        ('Child Faces', 2),
        ('Adult Voices', 3),
        ('Child Voices', 4)
        ],
    default=0,
    open_middle=False,  # Opens in the middle of the menu
    selection_box_height=10,
    selection_box_width=300,
    selection_infinite=True,
)

menu.add.button('Play', mainMenuState)
menu.add.button('Quit', pygame_menu.events.EXIT)

while displayMainMenu == True:
    events = pygame.event.get()
    menu.update(events)
    menu.draw(surface)
    pygame.display.update()