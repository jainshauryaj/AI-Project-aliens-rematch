import numpy as np
import random
import time

def update_neighbours(posX, posY, ship, dimension):
    """Update the neighbour cells of the given cell."""
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = posX + dx, posY + dy
        if 0 <= new_x < dimension and 0 <= new_y < dimension:
            ship[new_x, new_y, 1] += 1
    return ship

def valid_neighbours(posX, posY, ship, dimension):
    """Return a list of valid neighbours of the given cell."""
    valid_list = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = posX + dx, posY + dy
        if 0 <= new_x < dimension and 0 <= new_y < dimension and ship[new_x, new_y, 0] == 0:
            valid_list.append([new_x, new_y])
    return valid_list

def open_random_cell(one_adj_list_temp, ship, dimension):
    """Open a random cell from the list of cells."""
    posX, posY = random.choice(one_adj_list_temp)
    ship[posX, posY, 0] = 1
    update_neighbours(posX, posY, ship, dimension)
    return ship

def generate_ship(dim):
    """Generate the ship layout."""
    start_time = time.time()
    ship = np.zeros([dim, dim, 2], dtype=int)    
    posX, posY = np.random.randint(dim, size=2)
    ship[posX, posY, 0] = 1
    ship = update_neighbours(posX, posY, ship, dim)

    while True:
        one_adj_list = np.where(ship[:,:,1] == 1)
        one_adj_list = list(zip(one_adj_list[0], one_adj_list[1]))
        one_adj_list_temp = [i for i in one_adj_list if ship[i[0], i[1], 0] == 0]
        if not one_adj_list_temp:
            break
        ship = open_random_cell(one_adj_list_temp, ship, dim)

    dead_list = np.where(ship[:,:,1] == 1)
    dead_list = list(zip(dead_list[0], dead_list[1]))
    half_dead = random.sample(dead_list, len(dead_list)//2)

    for i in half_dead:
        posX, posY = i
        valid_adj = valid_neighbours(posX, posY, ship, dim)
        if valid_adj:
            opX, opY = random.choice(valid_adj)
            ship[opX, opY, 0] = 1
            ship = update_neighbours(opX, opY, ship, dim)

    end_time = time.time()
    time_taken = end_time - start_time
    return np.matrix(ship[:,:,0]), time_taken