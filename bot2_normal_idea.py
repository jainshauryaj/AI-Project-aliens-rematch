"""

Game Initialization: The game is initialized with a 50x50 ship, 6 aliens, and 1 crew member. The initialize_game function returns the bot, the list of aliens, the list of crew members, and the ship.

Printing Initial Positions: The initial positions of the bot, aliens, and crew members are printed out. This is done using a for loop that goes through each alien and crew member and prints their position.

Probability Matrices: For Bot 2, we create two probability matrices - one for the alien and one for the crew member. These matrices represent the bot's belief about where the alien and crew member might be. Initially, the bot assumes that the alien and crew member are equally likely to be in any cell.

Updating Probabilities: At each timestep, the bot updates its belief about the positions of the alien and crew member. This is done in two steps:

        Sensor Update: The bot updates its belief based on its sensors. For simplicity, we're assuming that the bot's sensors tell it the exact positions of the alien and crew member. In a more realistic scenario, the bot's sensors might be imperfect and the bot would have to update its belief based on the likelihood of the sensor readings given the true positions of the alien and crew member.
        Motion Update: The bot updates its belief about the alien's position based on the alien's possible movements. We're assuming that the alien can move to any adjacent cell with equal probability.

Choosing the Next Move: The bot chooses its next move to maximize the probability of finding the crew member while strongly avoiding the alien. The bot considers all possible moves and chooses the one that maximizes the difference between the crew member probability and 100 times the alien probability. The factor of 100 represents the bot's preference for avoiding the alien over finding the crew member.

Moving the Bot: The bot moves to the chosen cell.

Printing the Current State: The current state of the game, including the time, the positions of the bot, alien, and crew member, is printed out.

This process is repeated for 100 timesteps.

"""


import numpy as np
import ship_generation
import alien_bot_crew_movement

# Generate a 50x50 ship
ship, time_taken = ship_generation.generate_ship(50)

# Initialize the game
bot, aliens, crew_members, ship = alien_bot_crew_movement.initialize_game(ship, k = 5, num_aliens = 1, num_crew = 1)

# Initialize the probabilities
alien_probs = np.ones_like(ship) / np.count_nonzero(ship == 1)
crew_probs = np.ones_like(ship) / np.count_nonzero(ship == 1)
alien_probs[bot.position] = 0
crew_probs[bot.position] = 0

# Run the game
for t in range(100):  # Run for 100 timesteps
    # Update the probabilities based on the bot's sensors
    # For now, let's assume the bot's sensors tell it the exact positions of the alien and crew member
    alien_probs = np.zeros_like(ship)
    alien_probs[aliens[0].position] = 1
    crew_probs = np.zeros_like(ship)
    crew_probs[crew_members[0].position] = 1

    # Update the probabilities based on the alien's possible movements
    # For now, let's assume the alien can move to any adjacent cell with equal probability
    new_alien_probs = np.zeros_like(ship)
    for x in range(ship.shape[0]):
        for y in range(ship.shape[1]):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= x + dx < ship.shape[0] and 0 <= y + dy < ship.shape[1]:
                    new_alien_probs[x + dx, y + dy] += alien_probs[x, y] / 4
    alien_probs = new_alien_probs

    # Choose the next move
    possible_moves = [(bot.position[0] + dx, bot.position[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= bot.position[0] + dx < ship.shape[0] and 0 <= bot.position[1] + dy < ship.shape[1]]
    best_move = max(possible_moves, key=lambda pos: crew_probs[pos] - 100 * alien_probs[pos])

    # Move the bot
    bot.position = best_move

    # Print the current state
    print(f"Time: {t}")
    print("Bot position:", bot.position)
    print("Alien position:", aliens[0].position)
    print("Crew member position:", crew_members[0].position)
    print()