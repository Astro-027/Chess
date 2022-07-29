import pygame
from pathlib import Path

##########
# Pygame #
##########
WIDTH = 1280
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.init()

#########
# Paths #
#########
FILE_PATH = Path(__file__).parent.absolute()
ASSETS_PATH = str(FILE_PATH / "Assets") + "/"
IMAGES_PATH = ASSETS_PATH + "Images" + "/"
FONTS_PATH = ASSETS_PATH + "Fonts" + "/"

#########
# Fonts #
#########
#SIZES = {'small' : 20, 'medium' : 40, 'large' : 60}
FONTS = { 'Regular' : FONTS_PATH + "PressStart2P-Regular.ttf", 'Timer' : FONTS_PATH + "alarm_clock.ttf"}
SYS_FONTS = pygame.font.get_fonts()
def GET_FONT(name: str, size: int):
    '''Returns the @name pygame font of @size size.'''
    if name in SYS_FONTS:
        return pygame.font.SysFont(name, size)
    return pygame.font.Font(FONTS[name], size)

##########
# Colors #
##########
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (116, 252, 152, 230)
RED = (244, 66, 66)
DARK_RED = "#880015"
LIGHT_BROWN = "#b97a57"
BROWN = "#724E2F"
GOLD_HIGHLIGHT = "#F6F456"
GOLD = "#E6CC39"
GOLD_SHADOW = "#918A20"
TAN = "#C9AD71"
GREY = "#99958D"
ORANGE = "#b68f40"

##########
# Images #
##########
BACKGROUND = pygame.image.load(IMAGES_PATH + "brain_colorful.jpg")




PLAYER_F = pygame.font.SysFont('brushscript', 62)
# TIMER_F