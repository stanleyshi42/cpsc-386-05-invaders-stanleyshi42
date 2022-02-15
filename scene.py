# Stanley Shi
# CPSC 386-01
# 2021-11-24
# stanleyshi@csu.fullerton.edu
# @stanleyshi42
#
# Lab 05
#
# Classes for each Scene of the game
#

"""Classes for each Scene of the game"""

from datetime import date
import json
import os
import pygame
import game_objects


class Scene:
    """Scenes for the game"""

    def __init__(self, screen, background_color, next_scene=None, prev_scene=None):
        self._is_valid = True
        self._frame_rate = 60
        self._frame_count = 0
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background_color = background_color
        self._background.fill(self._background_color)
        self._next_scene = next_scene
        self._prev_scene = prev_scene

    def is_valid(self):
        """Returns if the scene is valid"""
        return self._is_valid

    def frame_rate(self):
        """Returns the scene's frame rate"""
        return self._frame_rate

    def update(self):
        """Updates the scene's data every tick"""
        self._frame_count += 1

    def draw(self):
        """Draws the scene every tick"""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process user input"""
        if event.type == pygame.QUIT:
            self._is_valid = False
            pygame.quit()


class TitleScene(Scene):
    """Scene for the Title Screen"""

    def __init__(self, screen, background_color, title, title_color, title_size):
        super().__init__(screen, background_color)
        self._next_scene = GameScene(screen, (0, 255, 255))

        # Create a Font for each group of text
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        instructions_font = pygame.font.Font(
            pygame.font.get_default_font(), int(title_size * 0.8)
        )

        # Render Title text
        (w, h) = self._screen.get_size()
        self._title = title_font.render(title, True, title_color)
        self._title_pos = self._title.get_rect(center=(w / 2, h / 4))

        # Render Instructions text
        instructions_text = "Move with the Arrow Keys"
        self._instructions1 = instructions_font.render(
            instructions_text, True, title_color
        )
        self._instructions_pos1 = self._instructions1.get_rect(center=(w / 2, h * 0.5))

        instructions_text = "Shoot with the Spacebar"
        self._instructions2 = instructions_font.render(
            instructions_text, True, title_color
        )
        self._instructions_pos2 = self._instructions2.get_rect(center=(w / 2, h * 0.6))

        instructions_text = "Hit Spacebar to start the game"
        self._instructions3 = instructions_font.render(
            instructions_text, True, title_color
        )
        self._instructions_pos3 = self._instructions3.get_rect(center=(w / 2, h * 0.7))

    def draw(self):
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._instructions1, self._instructions_pos1)
        self._screen.blit(self._instructions2, self._instructions_pos2)
        self._screen.blit(self._instructions3, self._instructions_pos3)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._is_valid = False


class GameScene(Scene):
    """Scene for the game of Snake"""

    def __init__(self, screen, background_color, score = 0, lives = 3):
        super().__init__(screen, background_color)
        (w, h) = self._screen.get_size()
        self._game = game_objects.SpaceInvaders(screen, score, lives)  # Instantiate the game

        # Render Score text
        score_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._score = score_font.render(
            "Score: " + str(self._game.points), True, (0, 0, 0)
        )
        self._score_pos = self._score.get_rect(center=(w * 0.2, h * 0.05))

        # Render Lives text
        lives_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._lives = lives_font.render(
            "Lives: " + str(self._game.lives), True, (0, 0, 0)
        )
        self._lives_pos = self._lives.get_rect(center=(w * 0.8, h * 0.05))

    def process_event(self, event):
        super().process_event(event)
        # Process player input
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if self._game.player.x > 0:
                self._game.player.x -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if self._game.player.x < self._game.grid.max_x - 1:
                self._game.player.x += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._game.create_laser()

    def update(self):
        super().update()

        # Update the game state
        self._game.update(self._frame_count)

        # Update Score text
        score_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._score = score_font.render(
            "Score: " + str(self._game.points), True, (0, 0, 0)
        )

        # Update Lives text
        lives_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._lives = lives_font.render(
            "Lives: " + str(self._game.lives), True, (0, 0, 0)
        )

        # Check if Level Complete
        if self._game.level_complete:
            self.level_complete(self._screen)

        # Check for Game Over
        if self._game.game_over:
            self.game_over(self._screen, self._game.points)

    def draw(self):
        super().draw()

        # Draw score text
        self._screen.blit(self._score, self._score_pos)

        # Draw lives text
        self._screen.blit(self._lives, self._lives_pos)

        # Draw the player
        pygame.draw.rect(
            self._screen,
            (100, 100, 100),
            [
                self._game.player.x * self._game.grid.cell_size,
                self._game.player.y * self._game.grid.cell_size,
                self._game.grid.cell_size,
                self._game.grid.cell_size,
            ],
        )

        # Draw each space invader
        for invader in self._game.invaders:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                [
                    invader.x * self._game.grid.cell_size,
                    invader.y * self._game.grid.cell_size,
                    self._game.grid.cell_size,
                    self._game.grid.cell_size,
                ],
            )

        # Draw each player laser
        for laser in self._game.player_lasers:
            pygame.draw.rect(
                self._screen,
                laser.color,
                [
                    laser.x * self._game.grid.cell_size,
                    laser.y * self._game.grid.cell_size,
                    self._game.grid.cell_size,
                    self._game.grid.cell_size,
                ],
            )

        # Draw each invader laser
        for laser in self._game.invader_lasers:
            pygame.draw.rect(
                self._screen,
                laser.color,
                [
                    laser.x * self._game.grid.cell_size,
                    laser.y * self._game.grid.cell_size,
                    self._game.grid.cell_size,
                    self._game.grid.cell_size,
                ],
            )

        # Draw each obstacle
        for obstacle in self._game.obstacles:
            pygame.draw.rect(
                self._screen,
                obstacle.color,
                [
                    obstacle.x * self._game.grid.cell_size,
                    obstacle.y * self._game.grid.cell_size,
                    self._game.grid.cell_size,
                    self._game.grid.cell_size,
                ],
            )

    def level_complete(self, screen):
        black = (0,0,0)
        self._next_scene = LevelCompleteScene(screen, black, self._game.points, self._game.lives)
        self._is_valid = False

    def game_over(self, screen, score):
        # Write score data to file
        data = {"score": score, "date": date.today().strftime("%d/%m/%Y")}

        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, "data")
        print("Data directory:", data_dir)

        with open(data_dir + "/scores.json", "a") as outfile:
            json.dump(data, outfile, indent=4)

        # Move to Game Over scene
        self._next_scene = GameOverScene(screen, (20, 20, 20), score)
        self._is_valid = False


class LevelCompleteScene(Scene):
    """Scene for the Level Complete Screen"""

    def __init__(self, screen, background_color, score, lives):
        super().__init__(screen, background_color)
        self._score = score
        self._lives = lives
        (w, h) = screen.get_size()

        # Render text
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._level_compelte_text = font.render(
            "Level Complete!", True, (255, 255, 255)
        )
        self._level_compelte_pos = self._level_compelte_text.get_rect(
            center=(w / 2, h * 0.3)
        )

        self._next_level_text = font.render("[R] Next Level", True, (255, 255, 255))
        self._next_level_text_pos = self._next_level_text.get_rect(
            center=(w / 2, h * 0.5)
        )

    def draw(self):
        super().draw()
        self._screen.blit(self._level_compelte_text, self._level_compelte_pos)
        self._screen.blit(self._next_level_text, self._next_level_text_pos)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._next_scene = GameScene(self._screen, (0, 255, 255), self._score, self._lives)
            self._is_valid = False


class GameOverScene(Scene):
    """Scene for the Game Over Screen"""

    def __init__(self, screen, background_color, score):
        super().__init__(screen, background_color)
        self._score = score
        (w, h) = screen.get_size()

        # Render text
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self._game_over_text = font.render("Game Over", True, (100, 0, 0))
        self._game_over_pos = self._game_over_text.get_rect(center=(w / 2, h * 0.1))

        self._score_text = font.render("Final Score: " + str(score), True, (0, 100, 0))
        self._score_text_pos = self._score_text.get_rect(center=(w / 2, h * 0.2))

        self._play_again_text = font.render("[R] Play Again", True, (200, 200, 200))
        self._play_again_text_pos = self._score_text.get_rect(center=(w / 2, h * 0.8))

        self._exit_text = font.render("[ESC] Quit", True, (200, 200, 200))
        self._exit_text_pos = self._score_text.get_rect(center=(w / 2, h * 0.9))

        # Get High Score data TODO
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, "data")
        high_scores = []

    def draw(self):
        super().draw()
        self._screen.blit(self._game_over_text, self._game_over_pos)
        self._screen.blit(self._score_text, self._score_text_pos)
        self._screen.blit(self._play_again_text, self._play_again_text_pos)
        self._screen.blit(self._exit_text, self._exit_text_pos)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._next_scene = GameScene(self._screen, (0, 255, 255))
            self._is_valid = False
