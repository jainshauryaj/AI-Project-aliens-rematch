# Python
import numpy as np
import random

def move_entity(position, direction, ship):
    new_position = list(position)
    if direction == 'up':
        new_position[0] -= 1
    elif direction == 'down':
        new_position[0] += 1
    elif direction == 'left':
        new_position[1] -= 1
    elif direction == 'right':
        new_position[1] += 1

    if (0 <= new_position[0] < ship.shape[0] and 0 <= new_position[1] < ship.shape[1] and ship[new_position[0], new_position[1]] == 1):
        return tuple(new_position)
    else:
        return position

def move_alien(position, ship):
    directions = ['up', 'down', 'left', 'right']
    random.shuffle(directions)

    for direction in directions:
        new_position = move_entity(position, direction, ship)
        if new_position != position:
            return new_position
    return position

def initialize_game(ship, k, num_aliens, num_crew):
    open_cells = list(zip(*np.where(ship == 1)))
    bot_position = random.choice(open_cells)
    ship[bot_position] = 5

    crew_positions = random.sample(open_cells, num_crew)
    crew_positions = [pos for pos in crew_positions if pos != bot_position]
    for crew_position in crew_positions:
        ship[crew_position] = 9

    alien_positions = random.sample(open_cells, num_aliens)
    alien_positions = [pos for pos in alien_positions if abs(pos[0] - bot_position[0]) > k or abs(pos[1] - bot_position[1]) > k]
    for alien_position in alien_positions:
        ship[alien_position] = 7

    return bot_position, alien_positions, crew_positions, ship