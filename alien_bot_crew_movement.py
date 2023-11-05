import numpy as np
import random

class Bot:
    def __init__(self, position):
        self.position = position

    def move(self, direction, ship):
        new_position = list(self.position)
        if direction == 'up':
            new_position[0] -= 1
        elif direction == 'down':
            new_position[0] += 1
        elif direction == 'left':
            new_position[1] -= 1
        elif direction == 'right':
            new_position[1] += 1

        if (0 <= new_position[0] < ship.shape[0] and 0 <= new_position[1] < ship.shape[1] and ship[new_position[0], new_position[1]] == 1):
            self.position = tuple(new_position)

class Alien:
    def __init__(self, position):
        self.position = position

    def move(self, ship):
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)

        for direction in directions:
            new_position = list(self.position)
            if direction == 'up':
                new_position[0] -= 1
            elif direction == 'down':
                new_position[0] += 1
            elif direction == 'left':
                new_position[1] -= 1
            elif direction == 'right':
                new_position[1] += 1

            if (0 <= new_position[0] < ship.shape[0] and 0 <= new_position[1] < ship.shape[1] and ship[new_position[0], new_position[1]] == 1):
                self.position = tuple(new_position)
                break

class CrewMember:
    def __init__(self, position):
        self.position = position

def initialize_game(ship, k, num_aliens, num_crew):
    open_cells = list(zip(*np.where(ship == 1)))
    bot_position = random.choice(open_cells)
    bot = Bot(bot_position)
    ship[bot_position] = 5

    crew_positions = random.sample(open_cells, num_crew)
    crew_members = [CrewMember(pos) for pos in crew_positions if pos != bot_position]
    for crew_member in crew_members:
        ship[crew_member.position] = 9

    alien_positions = random.sample(open_cells, num_aliens)
    alien_positions = [pos for pos in alien_positions if abs(pos[0] - bot_position[0]) > k and abs(pos[1] - bot_position[1]) > k]
    aliens = [Alien(pos) for pos in alien_positions]
    for alien in aliens:
        ship[alien.position] = 7

    return bot, aliens, crew_members, ship