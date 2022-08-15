from distutils.log import info
import pygame
import sys
 
from config import *
from player import *
from board import *
from _backend.accessory import *
 
 
class SceneManager:
   '''A stack of Scene objects that can pop/push next scene to top.'''
   def __init__(self, players: [Player]):
       self.players = players
       self.scenes = []
 
   def enter(self):
       pass
 
   def exit(self):
       pass
 
   def input(self, event):
       if self.scenes:
           self.scenes[-1].input(event)
 
   def draw(self, screen):
       if self.scenes:
           self.scenes[-1].draw(screen)
 
   def push(self, scene):
       if self.scenes:
           self.scenes[-1].exit()
 
       self.scenes.append(scene)
       self.scenes[-1].enter()
 
   def pop(self):
       self.exit()
       self.scenes.pop()
       self.enter()
 
   def set(self, scene):
       self.scenes = [scene]
 
 
############
# Abstract #
############
class Scene:
   def __init__(self):
       pass
 
   def input(self, event):
       pass
 
   def draw(self, screen):
       pass
 
   def enter(self):
       pass
 
   def exit(self):
       pass
 
 
#############
# Main Menu #
#############
class MainMenuScene(Scene):
   def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 100)
       self.text = font.render("MAIN MENU", True, ORANGE)
       self.text_rect = self.text.get_rect(center=(640, 100))
 
       self.text_shadow = font.render("MAIN MENU", True, WHITE)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))
 
       font = GET_FONT('Regular', 75)
       self.play = Button(None, (640, 275), "PLAY", font, ORANGE, WHITE)
       self.play_shadow = font.render("PLAY", True, WHITE)
       self.play_shadow_rect = self.play_shadow.get_rect(center=(644, 279))
 
       self.options = Button(None, (640, 440), "OPTIONS", font, ORANGE, WHITE)
       self.options_shadow = font.render("OPTIONS", True, WHITE)
       self.options_shadow_rect = self.options_shadow.get_rect(center=(644, 444))
 
       self.quit = Button(None, (640, 600), "QUIT", font, ORANGE, WHITE)
       self.quit_shadow = font.render("QUIT", True, WHITE)
       self.quit_shadow_rect = self.quit_shadow.get_rect(center=(644, 604))
 
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.play.input(mouse_pos):
               scene = PlayerSelection(self.manager)
               self.manager.push(scene)
           elif self.options.input(mouse_pos):
               scene = Options(self.manager)
               self.manager.push(scene)
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
       self.play.set_color(mouse_pos)
       self.options.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
   def draw(self, screen):
       pygame.display.set_caption("Main Menu")
       screen.blit(BACKGROUND, (0, 0))
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.play_shadow, self.play_shadow_rect)
       screen.blit(self.options_shadow, self.options_shadow_rect)
       screen.blit(self.quit_shadow, self.quit_shadow_rect)
 
       self.play.update(screen)
       self.options.update(screen)
       self.quit.update(screen)
 
#############
# Selection #
#############
class PlayerSelection(Scene):
   def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 85)
       self.game_selection = font.render("PLAYER OPTIONS", True, ORANGE)
       self.game_selection_rect = self.game_selection.get_rect(center=(640, 100))
       self.game_selection_shadow = font.render("PLAYER OPTIONS", True, WHITE)
       self.game_selection_shadow_rect = self.game_selection_shadow.get_rect(center=(644, 104))
 
       font = GET_FONT('Regular', 75)
       self.one_player = Button(None, (640, 275), "One Player", font, ORANGE, WHITE)
       self.one_player_shadow = font.render("One Player", True, WHITE)
       self.one_player_rect = self.one_player_shadow.get_rect(center=(644, 279))
 
       self.two_player = Button(None, (640, 450), "Two Player", font, ORANGE, WHITE)
       self.two_player_shadow = font.render("Two Player", True, WHITE)
       self.two_player_rect = self.two_player_shadow.get_rect(center=(644, 454))
 
       font = GET_FONT('Regular', 65)
       self.back = Button(None, (340, 660), "BACK", font, ORANGE, WHITE)
       self.back_shadow = font.render("BACK", True, WHITE)
       self.back_rect = self.back_shadow.get_rect(center=(344, 664))
 
       self.quit = Button(None, (940, 660), "QUIT", font, ORANGE, WHITE)
       self.quit_shadow = font.render("QUIT", True, WHITE)
       self.quit_rect = self.back_shadow.get_rect(center=(944, 664))
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
          
           if self.one_player.input(mouse_pos) or self.two_player.input(mouse_pos):
               if self.one_player.input(mouse_pos):
                   self.manager.players[1] = Computer()
                   self.manager.players[2] = None
                   self.manager.players[3] = None
               else:
                   self.manager.players[1] = Human('Player 2')
                   self.manager.players[2] = None
                   self.manager.players[3] = None
 
               scene = TimeSelection(self.manager)
               self.manager.push(scene)
          
           elif self.back.input(mouse_pos):
               self.manager.pop()
              
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
          
 
       self.one_player.set_color(mouse_pos)
       self.two_player.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
       self.back.set_color(mouse_pos)
 
   def draw(self, screen):
       pygame.display.set_caption("Society of Overthinker's Chess")
       screen.fill(BLACK)
 
       screen.blit(self.game_selection_shadow, self.game_selection_shadow_rect)
       screen.blit(self.game_selection, self.game_selection_rect)
       screen.blit(self.one_player_shadow, self.one_player_rect)
       screen.blit(self.two_player_shadow, self.two_player_rect)
       screen.blit(self.back_shadow, self.back_rect)
       screen.blit(self.quit_shadow, self.quit_rect)
 
 
       self.one_player.update(screen)
       self.two_player.update(screen)
       self.quit.update(screen)
       self.back.update(screen)
 
 
class TimeSelection(Scene):
   def __init__(self, manager):
       self.manager = manager
 
       # get w/h and check % initial WIDTH/HEIGHT
       font = GET_FONT('Regular', 50)
       self.text = font.render("CHOOSE YOUR TIMER OPTION", True, ORANGE)
       self.text_rect = self.text.get_rect(center=(640, 50))
       self.text_shadow = font.render("CHOOSE YOUR TIMER OPTION", True, BLACK)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 54))
 
       font = GET_FONT('Regular', 25)
       time_1_0 = Two_Line(None, (225, 200), "BULLET", "1 + 0", font, ORANGE, BLACK)
       time_2_1 = Two_Line(None, (640, 200), "BULLET", "2 + 1", font, ORANGE, BLACK)
       time_3_0 = Two_Line(None, (1055, 200), "BLITZ", "3 + 0", font, ORANGE, BLACK)
       time_3_2 = Two_Line(None, (225, 340), "BLITZ", "3 + 0", font, ORANGE, BLACK)
       time_5_0 = Two_Line(None, (640, 340), "BLITZ", "5 + 0", font, ORANGE, BLACK)
       time_5_3 = Two_Line(None, (1055, 340), "BLITZ", "5 + 3", font, ORANGE, BLACK)
       time_10_0 = Two_Line(None, (225, 475), "RAPID", "10 + 0", font, ORANGE, BLACK)
       time_10_5 = Two_Line(None, (640, 475), "RAPID", "10 + 5", font, ORANGE, BLACK)
       time_15_10 = Two_Line(None, (1055, 475), "RAPID", "15 + 10", font, ORANGE, BLACK)
       self.buttons = (time_1_0, time_2_1, time_3_0, time_3_2, time_5_0, time_5_3, time_10_0, time_10_5, time_15_10)
 
       font = GET_FONT('Regular', 40)
       self.time_unlimited = Button(None, (644, 620), "UNLIMITED", font, ORANGE, BLACK)
       self.time_unlimited_shadow = font.render("UNLIMITED", True, BLACK)
       self.time_unlimited_rect = self.time_unlimited_shadow.get_rect(center=(640, 623))
 
       font = GET_FONT('Regular', 50)
       self.back = Button(None, (100, 750), "<=", font, ORANGE, BLACK)
       self.back_shadow = font.render("<=", True, BLACK)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(103, 753))
 
       font = GET_FONT('Regular', 35)
       self.info = Button(None, (640, 750), "TIMER INFO", font, ORANGE, BLACK)
       self.info_shadow = font.render("TIMER INFO", True, BLACK)
       self.info_shadow_rect = self.info_shadow.get_rect(center=(644, 753))
 
       self.quit = Button(None, (1140, 750), "QUIT", font, ORANGE, BLACK)
       self.quit_shadow = font.render("QUIT", True, BLACK)
       self.quit_rect = self.quit_shadow.get_rect(center=(1144, 753))
      
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
 
       if event.type == pygame.MOUSEBUTTONDOWN:
          
           for button in self.buttons:
               if button.input(mouse_pos):
                   time = self._parse_time(button.name)
 
                   self.manager.pop() # PlayerSelection
                   scene = Game(self.manager, time)
                   self.manager.push(scene)
                  
           if self.time_unlimited.input(mouse_pos):
               self.manager.pop() # PlayerSelection
               scene = Game(self.manager)
               self.manager.push(scene)
              
           elif self.back.input(mouse_pos):
               self.manager.pop()
           
           elif self.info.input(mouse_pos):
               self.manager.pop()
               scene = TimerInfo(self.manager)
               self.manager.push(scene)  
              
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
 
 
       for button in self.buttons:
           button.set_color(mouse_pos)
 
       self.time_unlimited.set_color(mouse_pos)
       self.back.set_color(mouse_pos)
       self.info.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
 
   def draw(self, screen):
       pygame.display.set_caption("Time Selection")
       screen.fill(WHITE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
 
       for button in self.buttons:
           button.update(screen)
      
       self.time_unlimited.update(screen)
       screen.blit(self.time_unlimited_shadow, self.time_unlimited_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
       screen.blit(self.info_shadow, self.info_shadow_rect)
       self.info.update(screen)
       screen.blit(self.quit_shadow, self.quit_rect)
       self.quit.update(screen)
 
   def _parse_time(self, name: str) -> (int, int):
       if len(name) == 5:
           return (int(name[0]), int(name[-1]))
       elif len(name) == 6:
           return (int(name[:2]), int(name[-1]))
       else:
           return (int(name[:2]), int(name[-2:]))
 
 
 
class TimerInfo(TimeSelection):
   def __init__(self, manager):
       self.manager = manager
 
       # get w/h and check % initial WIDTH/HEIGHT
       font = GET_FONT('Regular', 50)
       self.text = font.render("TIMER INFO", True, ORANGE)
       self.text_rect = self.text.get_rect(center=(640, 75))
       self.text_shadow = font.render("TIMER INFO", True, BLACK)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 79))
       self.back = Button(None, (100, 700), "<=", font, ORANGE, BLACK)
       self.back_shadow = font.render("<=", True, BLACK)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(103, 703))
 
       font = GET_FONT('Regular', 20)
       self.info = font.render("Time controls are based on estimated game duration", True, BLACK)
       self.info_rect = self.info.get_rect(center=(640, 180))
 
       # Triple quoted strings contain new line characters
       self.t_text = font.render("(clock initial time in seconds) + 40 × (clock increment)", True, BLACK)
       self.t_text_rect = self.t_text.get_rect(center=(640, 225))
 
       font = GET_FONT('Regular', 30)
       self.bullet = font.render("≤ 179s = Bullet", True, BLACK)
       self.bullet_rect = self.bullet.get_rect(center=(640, 350))
 
       self.blitz = font.render("≤ 479s = Blitz", True, BLACK)
       self.blitz_rect = self.blitz.get_rect(center=(640, 450))
 
       self.rapid = font.render("≤ 1499s = Rapid", True, BLACK)
       self.rapid_rect = self.rapid.get_rect(center=(640, 550))
 
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()
 
 
       self.back.set_color(mouse_pos)
 
   def draw(self, screen):
       pygame.display.set_caption("Timer Info")
       screen.fill(WHITE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.info, self.info_rect)
       screen.blit(self.t_text, self.t_text_rect)
       screen.blit(self.bullet, self.bullet_rect)
       screen.blit(self.blitz, self.blitz_rect)
       screen.blit(self.rapid, self.rapid_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
 
 
#############
# Game Play #
#############
class Game(Scene):
   def __init__(self, manager, time=(0, 0)):
       '''For timed and untimed chess matches.'''
       self.manager = manager
       self.time = time
       pygame.time.set_timer(pygame.USEREVENT, 1000)
 
       if self.time == (0, 0): # Unlimited Time
           self.timer_1 = None
           self.timer_2 = None
       else:
           self.timer_1 = Timer(self.manager, self.time[0], self.time[1])
           self.timer_2 = Timer(self.manager, self.time[0], self.time[1])
      
       # Logo Text
       font = GET_FONT("elephant", 54)
       self.retro_text = font.render("Retro", True, GOLD)
       self.modern_text = font.render("Modern", True, GOLD)
       self.chess_text = font.render("Chess", True, GOLD)
      
       # Menu Buttons
       font = GET_FONT("ocr", 58)
       self.menu_text = font.render("Menu", True, BLACK, GREY)
       self.exit_text = font.render("Exit", True, BLACK, GREY)
      
       # Board
       self.board = Board(self.manager)
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.USEREVENT:
           if self.board.current_turn == 0:
               self.timer_1.update()
           if self.board.current_turn == 1:
               self.timer_2.update()
       mouse_pos = pygame.mouse.get_pos()
       self.board.input(event)
 
   def draw(self, screen):
       pygame.display.set_caption("Retro|Modern Chess")
       screen.fill(BLACK)
 
       wing_width = screen.get_width() * .20
       wing_height = screen.get_height()
 
       left_wing = pygame.Rect(0, 0, wing_width, wing_height)
       right_wing = pygame.Rect(0, 0, wing_width, wing_height)
       left_wing.topleft = (0, 0)
       right_wing.right = screen.get_width()
 
       pygame.draw.rect(screen, GOLD, left_wing, 6)
       pygame.draw.rect(screen, GOLD, right_wing, 6)
 
       # Game Frame
       self._draw_frame(screen, left_wing, right_wing)
      
       # Retro|Modern Chess text
       screen.blit(self.retro_text, self.retro_text.get_rect(center=(left_wing.centerx, screen.get_height() * .81)))
       screen.blit(self.modern_text, self.modern_text.get_rect(center=(left_wing.centerx, screen.get_height() * .87)))
       screen.blit(self.chess_text, self.chess_text.get_rect(center=(left_wing.centerx, screen.get_height() * .93)))
      
       # Timer
       if self.time != (0, 0):
           self._add_timer_rects(screen, left_wing, right_wing)
           self.timer_1.draw(screen, left_wing.center, 32)
           self.timer_2.draw(screen, right_wing.center, 32)
 
       # Menu Buttons
       screen.blit(self.menu_text, self.menu_text.get_rect(center=(right_wing.centerx, right_wing.height * .82)))
       screen.blit(self.exit_text, self.exit_text.get_rect(center=(right_wing.centerx, right_wing.height * .92)))
      
       # Player Names
       self._add_player_text(screen, left_wing, self.manager.players[0].name)
       self._add_player_text(screen, right_wing, self.manager.players[1].name)
      
       # Board
       self.board.draw(screen)
      
   def _draw_frame(self, screen, left_wing, right_wing):
       self._add_wings(screen, left_wing, right_wing)
       self._add_graveyard(screen, left_wing, right_wing)
 
   def _add_wings(self, screen,left_wing, right_wing):
       '''Adds shadows and highlights to the decorative elements of the gamebox.'''
       # Shadows
       left_shadow = pygame.Rect(0, 0,(left_wing.width * .99), (left_wing.height * .994))
       right_shadow = pygame.Rect(0, 0, (right_wing.width * .99), (right_wing.height * .994))
       left_shadow.left = left_wing.left + 5
       left_shadow.top = left_wing.top + 5
       right_shadow.left = right_wing.left + 5
       right_shadow.top = right_wing.top + 5
 
       pygame.draw.rect(screen, GOLD_SHADOW, left_shadow, 3)
       pygame.draw.rect(screen, GOLD_SHADOW, right_shadow, 3)
      
       # Highlight
       left_highlight = pygame.Rect(0, 0, left_wing.width * .99, left_wing.height * .995)
       right_highlight = pygame.Rect(0, 0, right_wing.width * .99, right_wing.height * .995)
       left_highlight.topleft = left_wing.topleft
       right_highlight.topleft = right_wing.topleft
 
       pygame.draw.rect(screen, WHITE, left_highlight, 1)
       pygame.draw.rect(screen, WHITE, right_highlight, 1)
      
   def _add_graveyard(self, screen, left_wing, right_wing):
       '''Adds blank rectangles with shadows to hold captured pieces.'''
       left_graveyard = pygame.Rect(0, 0, left_wing.width * .75, left_wing.height * .5)
       right_graveyard = pygame.Rect(0, 0, right_wing.width * .75, right_wing.height * .5)
       left_graveyard.center = left_wing.center
       right_graveyard.center = right_wing.center
 
       pygame.draw.rect(screen, GOLD, left_graveyard, 4)
       pygame.draw.rect(screen, GOLD, right_graveyard, 4)
      
       # Shadows
       left_shadow = pygame.Rect(0, 0, left_graveyard.width * .99, left_graveyard.height * .99)
       right_shadow = pygame.Rect(0, 0, right_graveyard.width * .99, right_graveyard.height * .99)
       left_shadow.left = left_graveyard.left + 3
       left_shadow.top = left_graveyard.top + 2
       right_shadow.left = right_graveyard.left + 3
       right_shadow.top = right_graveyard.top + 2
 
       pygame.draw.rect(screen, GOLD_SHADOW, left_shadow, 2)
       pygame.draw.rect(screen, GOLD_SHADOW, right_shadow, 2)
 
   def _add_timer_rects(self, screen, left_wing, right_wing):
       '''Adds blank rectangles to hold the player timers.'''
       l_timer_rect = pygame.Rect(0, 0, left_wing.width * .75, left_wing.height * .09)
       r_timer_rect = pygame.Rect(0, 0, right_wing.width * .75, right_wing.height * .09)
       l_timer_rect.centerx = left_wing.centerx
       r_timer_rect.centerx = right_wing.centerx
       l_timer_rect.centery = left_wing.centery * .38
       r_timer_rect.centery = right_wing.centery * .38
 
       pygame.draw.rect(screen, GOLD, l_timer_rect, 4)
       pygame.draw.rect(screen, GOLD, r_timer_rect, 4)
      
       # Shadows
       l_shadow = pygame.Rect(0, 0,l_timer_rect.width * .99, l_timer_rect.height * .99)
       r_shadow = pygame.Rect(0, 0,r_timer_rect.width * .99, r_timer_rect.height * .99)
       l_shadow.left = l_timer_rect.left+2
       r_shadow.left = r_timer_rect.left + 2
       l_shadow.top = l_timer_rect.top + 2
       r_shadow.top = r_timer_rect.top + 2
 
       pygame.draw.rect(screen, GOLD_SHADOW, l_shadow, 2)
       pygame.draw.rect(screen, GOLD_SHADOW, r_shadow, 2)
 
   def _add_player_text(self, screen, placement, title):
       '''Adds text, either "Player" or "Player 1", to the upper left corner of the gamebox.'''
       playersFont = GET_FONT('brushscript', 62)
       player_text = playersFont.render(title, True, GOLD)
       player_text_rect = player_text.get_rect()
       player_text_rect.centerx = placement.centerx
       player_text_rect.centery = placement.height * .08
 
       screen.blit(player_text, player_text_rect)
 
 
class Options(Scene):
   def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 100)
       self.text = font.render("OPTIONS", True, ORANGE)
       self.text_rect = self.text.get_rect(center=(640, 160))
       self.text_shadow = font.render("OPTIONS", True, BLACK)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 164))
 
       font = GET_FONT('Regular', 65)
       self.options = Button(None, (640, 375), "GAME OPTIONS", font, ORANGE, BLACK)
       self.options_shadow = font.render("GAME OPTIONS", True, BLACK)
       self.options_rect = self.options_shadow.get_rect(center=(644, 379))
       
       self.credits = Button(None, (640, 550), "CREDITS", font, ORANGE, BLACK)
       self.credits_shadow = font.render("CREDITS", True, BLACK)
       self.credits_rect = self.credits_shadow.get_rect(center=(644, 554))
 
       font = GET_FONT('Regular', 55)
       self.back = Button(None, (640, 750), "BACK", font, ORANGE, BLACK)
       self.back_shadow = font.render("BACK", True, BLACK)
       self.back_rect = self.back_shadow.get_rect(center=(644, 754))
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
 
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.options.input(mouse_pos):
               scene = GameOptions(self.manager)
               self.manager.push(scene)
               
           if self.credits.input(mouse_pos):
               scene = Credits(self.manager)
               self.manager.push(scene)
               
           elif self.back.input(mouse_pos):
               self.manager.pop()  # close options menu
        
       self.options.set_color(mouse_pos)
       self.credits.set_color(mouse_pos)
       self.back.set_color(mouse_pos)
 
   def draw(self, screen):
       pygame.display.set_caption("Options")
       screen.fill(WHITE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.options_shadow, self.options_rect)
       screen.blit(self.credits_shadow, self.credits_rect)
       screen.blit(self.back_shadow, self.back_rect)
       
       self.options.update(screen)
       self.credits.update(screen)
       self.back.update(screen)
 
 
class Credits(Scene):
   def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 45)
       self.text = font.render("This game is presented by: ", True, BLACK)
       self.text_rect = self.text.get_rect(center=(655, 100))
       self.text_shadow = font.render("This game is presented by: ", True, WHITE)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(658, 102))
 
       font = GET_FONT('Regular', 40)
       self.name_1 = font.render("Ashley Butela", True, BLACK)
       self.name_1_rect = self.name_1.get_rect(center=(640, 220))
       self.name_2 = font.render("Amy Ciuffoletti", True, BLACK)
       self.name_2_rect = self.name_2.get_rect(center=(640, 295))
       self.name_3 = font.render("Mehmet Ozen", True, BLACK)
       self.name_3_rect = self.name_2.get_rect(center=(700, 370))
       self.name_4 = font.render("Jacob Sharp", True, BLACK)
       self.name_4_rect = self.name_2.get_rect(center=(700, 445))
       self.name_5 = font.render("Nabeyou Tadessa", True, BLACK)
       self.name_5_rect = self.name_2.get_rect(center=(640, 520))
 
       font = GET_FONT('Regular', 50)
       self.back = Button(None, (640, 640), "BACK", font, BLACK, WHITE)
       self.back_shadow = font.render("BACK", True, WHITE)
       self.back_rect = self.back_shadow.get_rect(center=(642, 642))
 
   def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()  # close credits menu
 
       self.back.set_color(mouse_pos)
 
   def draw(self, screen):
       pygame.display.set_caption("Credits")
       screen.fill(ORANGE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.name_1, self.name_1_rect)
       screen.blit(self.name_2, self.name_2_rect)
       screen.blit(self.name_3, self.name_3_rect)
       screen.blit(self.name_4, self.name_4_rect)
       screen.blit(self.name_5, self.name_5_rect)
       screen.blit(self.back_shadow, self.back_rect)
 
       self.back.update(screen)


class GameOptions(Scene):
    def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 85)
       self.text = font.render("GAME OPTIONS", True, WHITE)
       self.text_rect = self.text.get_rect(center=(640, 100))
       self.text_shadow = font.render("GAME OPTIONS", True, ORANGE)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))
       
       font = GET_FONT('Regular', 55) 
       self.theme = Button(None, (640, 300), "THEME SELECTION", font, WHITE, ORANGE)
       self.theme_shadow = font.render("THEME SELECTION", True, ORANGE)
       self.theme_shadow_rect = self.theme_shadow.get_rect(center=(644, 304))
       
       self.lang = Button(None, (640, 450), "LANGUAGE SELECTION", font, WHITE, ORANGE)
       self.lang_shadow = font.render("LANGUAGE SELECTION", True, ORANGE)
       self.lang_shadow_rect = self.lang_shadow.get_rect(center=(644, 454))

       self.access = Button(None, (640, 600), "ACCESSIBILITY SETTINGS", font, WHITE, ORANGE)
       self.access_shadow = font.render("ACCESSIBILITY SETTINGS", True, ORANGE)
       self.access_shadow_rect = self.access_shadow.get_rect(center=(644, 604))
       
       font = GET_FONT('Regular', 45)
       self.back = Button(None, (140, 750), "<=", font, WHITE, ORANGE)
       self.back_shadow = font.render("<=", True, ORANGE)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(144, 754))
 
       self.quit = Button(None, (1140, 750), "QUIT", font, WHITE, ORANGE)
       self.quit_shadow = font.render("QUIT", True, ORANGE)
       self.quit_rect = self.quit_shadow.get_rect(center=(1144, 754))
       
    def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()

           elif self.theme.input(mouse_pos):
               scene = ThemeSelection(self.manager)
               self.manager.push(scene)
            
           elif self.lang.input(mouse_pos):
               scene = LanguageSelection(self.manager)
               self.manager.push(scene)
            
           elif self.access.input(mouse_pos):
               scene = AccessSettings(self.manager)
               self.manager.push(scene)
                      
           elif self.back.input(mouse_pos):
               self.manager.pop()
               
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
 
       self.back.set_color(mouse_pos)
       self.theme.set_color(mouse_pos)
       self.lang.set_color(mouse_pos)
       self.access.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
    def draw(self, screen):
       pygame.display.set_caption("Game Options")
       screen.fill(BLACK)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.theme_shadow, self.theme_shadow_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
       self.theme.update(screen)
       screen.blit(self.lang_shadow, self.lang_shadow_rect)
       self.lang.update(screen)
       screen.blit(self.access_shadow, self.access_shadow_rect)
       self.access.update(screen)
       screen.blit(self.quit_shadow, self.quit_rect)
       self.quit.update(screen)



class ThemeSelection(GameOptions):
    def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 80)
       self.text = font.render("THEME SELECTION", True, WHITE)
       self.text_rect = self.text.get_rect(center=(640, 100))
       self.text_shadow = font.render("THEME SELECTION", True, ORANGE)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))
       
       font = GET_FONT('Regular', 55) 
       self.theme_shadow = font.render("TEXT", True, ORANGE)
       self.theme_shadow_rect = self.theme_shadow.get_rect(center=(640, 300))
       
       self.lang_shadow = font.render("TEXT", True, ORANGE)
       self.lang_shadow_rect = self.lang_shadow.get_rect(center=(640, 450))

       self.access_shadow = font.render("TEXT", True, ORANGE)
       self.access_shadow_rect = self.access_shadow.get_rect(center=(640, 600))
       
       font = GET_FONT('Regular', 45)
       self.back = Button(None, (140, 750), "<=", font, WHITE, ORANGE)
       self.back_shadow = font.render("<=", True, ORANGE)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(144, 754))
 
       self.quit = Button(None, (1140, 750), "QUIT", font, WHITE, ORANGE)
       self.quit_shadow = font.render("QUIT", True, ORANGE)
       self.quit_rect = self.quit_shadow.get_rect(center=(1144, 754))
       
    def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()
               
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
 
       self.back.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
    def draw(self, screen):
       pygame.display.set_caption("Theme Selection")
       screen.fill(BLACK)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.theme_shadow, self.theme_shadow_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
       screen.blit(self.lang_shadow, self.lang_shadow_rect)
       screen.blit(self.access_shadow, self.access_shadow_rect)
       screen.blit(self.quit_shadow, self.quit_rect)
       self.quit.update(screen)
 
 
class LanguageSelection(GameOptions):
    def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 70)
       self.text = font.render("LANGUAGE OPTIONS", True, WHITE)
       self.text_rect = self.text.get_rect(center=(640, 100))
       self.text_shadow = font.render("LANGUAGE OPTIONS", True, BLACK)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))
       
       font = GET_FONT('Regular', 55) 
       self.theme_shadow = font.render("TEXT", True, BLACK)
       self.theme_shadow_rect = self.theme_shadow.get_rect(center=(640, 300))
       
       self.lang_shadow = font.render("TEXT", True, BLACK)
       self.lang_shadow_rect = self.lang_shadow.get_rect(center=(640, 450))

       self.access_shadow = font.render("TEXT", True, BLACK)
       self.access_shadow_rect = self.access_shadow.get_rect(center=(640, 600))
       
       font = GET_FONT('Regular', 45)
       self.back = Button(None, (140, 750), "<=", font, WHITE, BLACK)
       self.back_shadow = font.render("<=", True, BLACK)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(144, 754))
 
       self.quit = Button(None, (1140, 750), "QUIT", font, WHITE, BLACK)
       self.quit_shadow = font.render("QUIT", True, BLACK)
       self.quit_rect = self.quit_shadow.get_rect(center=(1144, 754))
       
    def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()
 
                      
           elif self.back.input(mouse_pos):
               self.manager.pop()
               
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
 
       self.back.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
    def draw(self, screen):
       pygame.display.set_caption("Language Options")
       screen.fill(ORANGE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.theme_shadow, self.theme_shadow_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
       screen.blit(self.lang_shadow, self.lang_shadow_rect)
       screen.blit(self.access_shadow, self.access_shadow_rect)
       screen.blit(self.quit_shadow, self.quit_rect)
       self.quit.update(screen)
       
       
class AccessSettings(GameOptions):
    def __init__(self, manager):
       self.manager = manager
 
       font = GET_FONT('Regular', 55)
       self.text = font.render("ACCESSIBILITY SETTINGS", True, BLACK)
       self.text_rect = self.text.get_rect(center=(640, 100))
       self.text_shadow = font.render("ACCESSIBILITY SETTINGS", True, ORANGE)
       self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))
       
       font = GET_FONT('Regular', 50) 
       self.theme_shadow = font.render("TEXT", True, ORANGE)
       self.theme_shadow_rect = self.theme_shadow.get_rect(center=(640, 300))
       
       self.lang_shadow = font.render("TEXT", True, ORANGE)
       self.lang_shadow_rect = self.lang_shadow.get_rect(center=(640, 450))

       self.access_shadow = font.render("TEXT", True, ORANGE)
       self.access_shadow_rect = self.access_shadow.get_rect(center=(640, 600))
       
       font = GET_FONT('Regular', 45)
       self.back = Button(None, (140, 750), "<=", font, BLACK, ORANGE)
       self.back_shadow = font.render("<=", True, ORANGE)
       self.back_shadow_rect = self.back_shadow.get_rect(center=(144, 754))
 
       self.quit = Button(None, (1140, 750), "QUIT", font, BLACK, ORANGE)
       self.quit_shadow = font.render("QUIT", True, ORANGE)
       self.quit_rect = self.quit_shadow.get_rect(center=(1144, 754))
       
    def input(self, event):
       mouse_pos = pygame.mouse.get_pos()
       if event.type == pygame.MOUSEBUTTONDOWN:
           if self.back.input(mouse_pos):
               self.manager.pop()
 
                      
           elif self.back.input(mouse_pos):
               self.manager.pop()
               
           elif self.quit.input(mouse_pos) or pygame.QUIT:
               pygame.quit()
               sys.exit()
 
       self.back.set_color(mouse_pos)
       self.quit.set_color(mouse_pos)
 
    def draw(self, screen):
       pygame.display.set_caption("Accessibility Settings")
       screen.fill(WHITE)
 
       screen.blit(self.text_shadow, self.text_shadow_rect)
       screen.blit(self.text, self.text_rect)
       screen.blit(self.theme_shadow, self.theme_shadow_rect)
       screen.blit(self.back_shadow, self.back_shadow_rect)
       self.back.update(screen)
       screen.blit(self.lang_shadow, self.lang_shadow_rect)
       screen.blit(self.access_shadow, self.access_shadow_rect)
       screen.blit(self.quit_shadow, self.quit_rect)
       self.quit.update(screen)