# Stanley Shi
# CPSC 386-01
# 2021-11-24
# stanleyshi@csu.fullerton.edu
# @stanleyshi42
#
# Lab 05
#
# A class for a game of Space Invaders
#

"""Game object for Space Invaders"""

import pygame
import scene


class InvadersGame:
    """A game of Space Invaders"""

    def __init__(self):
        pass

    def run(self):
        """Entry point to the game"""
        if not pygame.font:
            print("Warning: font disabled")
        if not pygame.mixer:
            print("Warning: sound disabled")
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data/encounter.wav")
        pygame.mixer.music.play(-1)

        window_size = (800, 800)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(window_size)
        title = "Space Invaders"
        pygame.display.set_caption(title)

        current_scene = scene.TitleScene(screen, (255, 255, 255), title, (0, 0, 0), 36)

        while current_scene.is_valid():
            clock.tick(current_scene.frame_rate())
            for event in pygame.event.get():
                current_scene.process_event(event)
            current_scene.update()
            current_scene.draw()
            pygame.display.update()
            # Go to next scene if the current scene is invalid
            if not current_scene.is_valid():
                if current_scene._next_scene:
                    current_scene = current_scene._next_scene
        pygame.quit()
        return 0
