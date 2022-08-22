import pygame
from pathlib import Path


##########
# Pygame #
##########
ASPECT_RATIO = (16, 10)
HEIGHT = 800
WIDTH = 1280
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.init()

def PIXEL_TO_ASPECT(width, height, aspect = ASPECT_RATIO):
    if width < height:
        width = abs(round(height / aspect[1])) * aspect[0] 
    else:
        height = abs(round(width / aspect[0])) * aspect[1]
    return width, height

def FIXED_SCALE(width, height, limit_min: tuple, limit_max: tuple):
    if width < limit_min[0]:
        width = limit_min[0]
    if height < limit_min[1]:
        height = limit_min[1]
    if width > limit_max[0]:
        width = limit_max[0]
    if height > limit_max[1]:
        height = limit_max[1]
    return width, height
#########
# Paths #
#########
FILE_PATH = Path(__file__).parent.absolute()
ASSETS_PATH = str(FILE_PATH / "Assets") + "/"
IMAGES_PATH = ASSETS_PATH + "Images/"
TEXTURE_PATH = ASSETS_PATH + "Textures/"
BLACK_TOP_PATH = ASSETS_PATH + "Pieces/Black/Top/"
WHITE_TOP_PATH = ASSETS_PATH + "Pieces/White/Top/"
BLACK_FRONT_PATH = ASSETS_PATH + "Pieces/Black/Front/"
WHITE_FRONT_PATH = ASSETS_PATH + "Pieces/White/Front/"
FONTS_PATH = ASSETS_PATH + "Fonts" + "/"

#########
# Fonts #
#########
#SIZES = {'small' : 20, 'medium' : 40, 'large' : 60}
FONTS = { 'Regular' : FONTS_PATH + "regular.ttf", 'Timer' : FONTS_PATH + "alarm_clock.ttf", 'elephant' : FONTS_PATH + "elephant.ttf", 'ocr' : FONTS_PATH + "ocr.ttf"}
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
LIGHT_GREEN = (116, 252, 152, 50)
RED = (244, 66, 66)
DARK_RED = ('#880015')
LIGHT_BROWN = ('#b97a57')
BROWN = ('#693F19')
GOLD_HIGHLIGHT = ('#F6F456')
GOLD = ('#FFD700')
GOLD_SHADOW = ('#91792F')
GREY = ('#99958D')
OAK = ('#DBA16A')
DARK_OAK = ('#341f0c')
ORANGE = ('#b68f40')
PURPLE = ('#cc5ced')

##########
# Images #
##########
BACKGROUND = pygame.image.load(IMAGES_PATH + "brain_colorful.jpg")

#################################
#       GRAVEYARD IMAGES        #
#################################

#Graveyard images
B_PAWN1 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN2 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN3 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN4 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN5 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN6 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN7 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_PAWN8 = pygame.image.load(BLACK_FRONT_PATH + "pawn_front.png")
B_BISHOP1 = pygame.image.load(BLACK_FRONT_PATH + "bishop_front.png")
B_BISHOP2 = pygame.image.load(BLACK_FRONT_PATH + "bishop_front.png")
B_ROOK1 = pygame.image.load(BLACK_FRONT_PATH + "rook_front.png")
B_ROOK2  = pygame.image.load(BLACK_FRONT_PATH + "rook_front.png")
B_KNIGHT1 = pygame.image.load(BLACK_FRONT_PATH + "knight_front.png")
B_KNIGHT2 = pygame.image.load(BLACK_FRONT_PATH + "knight_front.png")
B_QUEEN = pygame.image.load(BLACK_FRONT_PATH + "queen_front.png")
B_KING = pygame.image.load(BLACK_FRONT_PATH + "king_front.png")
W_PAWN1 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_PAWN2 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png") 
W_PAWN3 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_PAWN4 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png") 
W_PAWN5 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_PAWN6 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_PAWN7 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_PAWN8 = pygame.image.load(WHITE_FRONT_PATH + "pawn_front.png")
W_BISHOP1 = pygame.image.load(WHITE_FRONT_PATH + "bishop_front.png")
W_BISHOP2 = pygame.image.load(WHITE_FRONT_PATH + "bishop_front.png")
W_ROOK1 = pygame.image.load(WHITE_FRONT_PATH + "rook_front.png") 
W_ROOK2 = pygame.image.load(WHITE_FRONT_PATH + "rook_front.png")
W_KNIGHT1 = pygame.image.load(WHITE_FRONT_PATH + "knight_front.png") 
W_KNIGHT2 = pygame.image.load(WHITE_FRONT_PATH + "knight_front.png")
W_QUEEN = pygame.image.load(WHITE_FRONT_PATH + "queen_front.png")
W_KING = pygame.image.load(WHITE_FRONT_PATH + "king_front.png")