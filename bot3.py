"""



"""

def update_probabilities(bot, entity, ship, probs):
    # Calculate the expected sensor reading for each cell
    expected_sensor_readings = np.abs(np.indices(ship.shape) - np.array(bot.position)[:, None, None])

    # Calculate the difference between the expected and actual sensor readings
    sensor_diff = np.abs(expected_sensor_readings - bot.sensor(entity))

    # Update the probabilities
    probs = np.exp(-sensor_diff) * probs
    probs[ship == 0] = 0  # Set the probability to 0 for cells that are not part of the ship
    probs /= probs.sum()  # Normalize the probabilities so they sum to 1

    return probs

def choose_best_move(bot, crew_probs, alien_probs, ship):
    # Calculate the score for each cell
    scores = 2 * crew_probs - alien_probs  # Multiply crew_probs by 2 to prioritize them

    # Get the coordinates of the cells with the highest score
    best_moves = np.argwhere(scores == np.max(scores))

    # Choose one of the best moves at random
    best_move = best_moves[np.random.choice(best_moves.shape[0])]

    return tuple(best_move)


import numpy as np
import ship_generation
import alien_bot_crew_movement

# Generate a 50x50 ship
ship, time_taken = ship_generation.generate_ship(50)

# Initialize the game
bot, aliens, crew_members, ship = alien_bot_crew_movement.initialize_game(ship, k = 5, num_aliens = 1, num_crew = 1)

# Initialize the probabilities
alien_probs = np.ones_like(ship) / np.count_nonzero(ship == 1)
crew_probs = [np.ones_like(ship) / np.count_nonzero(ship == 1) for _ in range(2)]
for prob in crew_probs:
    prob[bot.position] = 0
alien_probs[bot.position] = 0

# Run the game
for t in range(100):  # Run for 100 timesteps
    # Update the probabilities based on the bot's sensors
    for i in range(2):
        if crew_members[i].position is not None:
            crew_probs[i] = update_probabilities(bot, crew_members[i], ship, crew_probs[i])
    alien_probs = update_probabilities(bot, aliens[0], ship, alien_probs)

    # Choose the next move
    combined_crew_probs = np.maximum(*crew_probs)
    best_move = choose_best_move(bot, combined_crew_probs, alien_probs, ship)

    # Move the bot
    bot.position = best_move

    # If the bot's position is the same as a crew member's position, teleport that crew member away
    for i in range(2):
        if bot.position == crew_members[i].position:
            crew_members[i].position = None
            crew_probs[i] = np.zeros_like(ship)

    # Print the current state
    print(f"Time: {t}")
    print("Bot position:", bot.position)
    print("Alien position:", aliens[0].position)
    print("Crew member position:", crew_members[0].position)
    print()