# Stanley Shi
# CPSC 386-01
# 2021-11-24
# stanleyshi@csu.fullerton.edu
# @stanleyshi42
#
# Lab 05
#
# Classes for objects in the game
#

"""Objects used for the game state of Space Invaders"""

import random


class Player:
    """The Player's entity"""

    def __init__(self, x, y):
        (self.x, self.y) = (x, y)  # Player's Coords


class Invader:
    """An Invader object"""

    def __init__(self, x: int, y: int, point_value: int):
        (self.x, self.y) = (x, y)  # Coords
        self.velocity = 1  # Direction the invader is moving; 1 = right, -1 = left
        self.steps = 0  # Counts steps made before changing directions
        self.point_value = point_value  # Amount of points awarded when hit

    def move(self):
        """Moves the invader"""

        if self.steps == 5:
            # Every 5 steps, change direction
            self.steps = 0  # Reset counter
            self.y += 1  # Move down by 1
            self.velocity *= -1  # Change directions
        else:
            # Move 1 step
            self.x += self.velocity
            self.steps += 1

    def coords(self):
        """Returns an invader's coords"""
        return (self.x, self.y)


class Laser:
    """A laser entity"""

    def __init__(self, x, y, velocity: int, color):
        (self.x, self.y) = (x, y)  # Coords
        self.color = color
        self.velocity = velocity  # Direction the laser is going; 1 = down, -1 = up

    def move(self):
        """Moves the laser in the direction it's moving"""
        self.y += self.velocity


class Obstacle:
    """An obstacle entity"""

    def __init__(self, x, y, color):
        (self.x, self.y) = (x, y)  # Coords
        self.color = color

    def coords(self):
        """Returns coords"""
        return (self.x, self.y)


class GameGrid:
    """The grid that the game is played on"""

    def __init__(self, screen):
        self.cell_size = 40  # Pixel width of the cells in the grid
        (w, h) = screen.get_size()
        self.max_x = int(w / self.cell_size)  # Number of cells in the x-axis
        self.max_y = int(h / self.cell_size)  # Number of cells in the y-axis


class SpaceInvaders:
    """Runs a game of Space Invaders"""

    def __init__(self, screen, points = 0, lives = 3):
        self.game_over = False
        self.level_complete = False  # Flag for if the player has destroyed all invaders
        self.grid = GameGrid(screen)
        self.player = Player(self.grid.max_x / 2, self.grid.max_y - 2)
        self.invaders = self.generate_invaders()  # Holds coords of each invader
        self.obstacles = self.generate_obstacles()  # Holds coords of obstacles
        self.player_lasers = []  # Holds coords of each player laser
        self.invader_lasers = []  # Holds coords of each invader laser
        self.lives = lives
        self.points = points

    def generate_invaders(self):
        """Instantiates each invader"""
        invaders = []
        point_value = 60
        for y in range(2, 7):
            point_value -= 10  # Change point value for each row of invaders
            for x in range(15):
                invaders.append(Invader(x, y, point_value))
        return invaders

    def generate_obstacles(self):
        obstacles = []
        white = (255, 255, 255)
        obstacles.append(Obstacle(3, 15, white))
        obstacles.append(Obstacle(4, 15, white))
        obstacles.append(Obstacle(9, 15, white))
        obstacles.append(Obstacle(10, 15, white))
        obstacles.append(Obstacle(15, 15, white))
        obstacles.append(Obstacle(16, 15, white))
        return obstacles

    def create_laser(self):
        """Adds a laser entity to the game"""
        x = self.player.x
        y = self.player.y - 1
        blue = (0, 0, 255)
        laser = Laser(x, y, -1, blue)
        self.player_lasers.append(laser)

    def update(self, frame_count):
        """Updates the game state"""
        # Update invaders every 60 frames
        if frame_count % 60 == 0:
            self.update_invaders()

        # Shoot an invader laser every 60 frames
        if frame_count % 40 == 0:
            self.invader_laser()

        # Update lasers every 5 frames
        if frame_count % 5 == 0:
            self.update_player_lasers()
            self.update_invader_lasers()

        # Check for Level Complete:
        if len(self.invaders) == 0:
            self.level_complete = True
            self.lives += 1 

        # Check for Game Over
        if self.lives == 0:
            self.game_over = True


    def update_player_lasers(self):
        """Updates each laser"""
        # Move each laser and checks for collisions
        for laser in self.player_lasers:
            (x, y) = (laser.x, laser.y)
            laser.move()

            # Check if laser hit an invader
            for invader in self.invaders:
                if (x, y) == invader.coords():
                    self.invaders.remove(invader)
                    self.player_lasers.remove(laser)
                    self.points += invader.point_value
                    break

            # Check if laser hit an obstacle
            for obstacle in self.obstacles:
                if (x, y) == obstacle.coords():
                    self.player_lasers.remove(laser)
                    break

            # Delete laser if it leaves the grid
            if laser.y < 0 | laser.y > self.grid.max_y:
                self.player_lasers.remove(laser)

    def update_invaders(self):
        """Updates each invader"""
        for invader in self.invaders:
            invader.move()
            # If an invader has reached the obstacles, trigger Game Over
            if invader.y == self.obstacles[0].y:
                self.game_over = True

    def invader_laser(self):
        """Shoot a laser from a random invader"""
        if len(self.invaders) > 0:
            rand = random.randint(0, len(self.invaders) - 1)
            invader = self.invaders[rand]
            x = invader.x
            y = invader.y
            red = (255, 0, 0)
            laser = Laser(x, y, 1, red)
            self.invader_lasers.append(laser)

    def update_invader_lasers(self):
        """Updates each laser"""
        # Move each laser and checks for collisions
        for laser in self.invader_lasers:
            laser.move()
            (x, y) = (laser.x, laser.y)

            # Check if player hit by laser
            if (x, y) == (self.player.x, self.player.y):
                self.invader_lasers.remove(laser)
                self.lives -= 1

            # Check if laser hit an obstacle
            for obstacle in self.obstacles:
                if (x, y) == obstacle.coords():
                    self.invader_lasers.remove(laser)
                    break

            # Delete laser if it leaves the grid
            if laser.y < 0 | laser.y > self.grid.max_y:
                self.player_lasers.remove(laser)        
    