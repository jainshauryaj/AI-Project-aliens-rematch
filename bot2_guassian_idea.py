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
    # Let's assume the bot's sensors give it the distance to the alien and crew member, with some noise
    alien_distance = np.abs(bot.position[0] - aliens[0].position[0]) + np.abs(bot.position[1] - aliens[0].position[1]) + np.random.normal(0, 1)
    crew_distance = np.abs(bot.position[0] - crew_members[0].position[0]) + np.abs(bot.position[1] - crew_members[0].position[1]) + np.random.normal(0, 1)
    for x in range(ship.shape[0]):
        for y in range(ship.shape[1]):
            alien_probs[x, y] *= np.exp(-0.5 * ((x - bot.position[0] + y - bot.position[1] - alien_distance) / 1)**2)
            crew_probs[x, y] *= np.exp(-0.5 * ((x - bot.position[0] + y - bot.position[1] - crew_distance) / 1)**2)
    alien_probs /= np.sum(alien_probs)
    crew_probs /= np.sum(crew_probs)

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