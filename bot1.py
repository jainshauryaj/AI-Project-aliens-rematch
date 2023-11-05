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

    # Choose the next move
    possible_moves = [(bot.position[0] + dx, bot.position[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= bot.position[0] + dx < ship.shape[0] and 0 <= bot.position[1] + dy < ship.shape[1]]
    best_move = max(possible_moves, key=lambda pos: crew_probs[pos] - alien_probs[pos])

    # Move the bot
    bot.position = best_move

    # Print the current state
    print(f"Time: {t}")
    print("Bot position:", bot.position)
    print("Alien position:", aliens[0].position)
    print("Crew member position:", crew_members[0].position)
    print()