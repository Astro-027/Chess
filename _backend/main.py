import pygame

from config import *
from scene import SceneManager, MainMenuScene
from player import *


def main():
    # Create Window
    pygame.init()
    screen = pygame.display.set_mode(PIXEL_TO_ASPECT(WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")

    # Create Player
    players = [Human('Player 1'), None]

    # Create Scene Manager
    manager = SceneManager(players)
    main_menu = MainMenuScene(manager)
    manager.push(main_menu)
    
    # Game Loop
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not manager.scenes:
                pygame.quit()
                running = False
            
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                width, height = FIXED_SCALE(width, height, (600, 400), (WIDTH, HEIGHT))
                width, height = PIXEL_TO_ASPECT(width, height)
                screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
            
            # Events
            manager.input(event)

        # Screen
        manager.draw(screen)
        pygame.display.update()

main()
