# Python
import numpy as np
import ship_generation
import alien_bot_crew_movement
# from alien_bot_crew_movement import Alien
import matplotlib.pyplot as plt

def bayesian_update(probs, beep, alpha, beta):
    likelihood = alpha if beep else 1 - alpha
    return probs * likelihood / (probs * likelihood + (1 - probs) * (1 - likelihood))

# Initialize counters
saves = 0
failures = 0

# Generate a 50x50 ship
ship, time_taken = ship_generation.generate_ship(50)

# Initialize the game
bot, aliens, crew_members, ship = alien_bot_crew_movement.initialize_game(ship, k = 5, num_aliens = 1, num_crew = 1)

# Initialize the probabilities
alien_probs = np.ones_like(ship, dtype=np.float64) / np.count_nonzero(ship == 1)
crew_probs = np.ones_like(ship, dtype=np.float64) / np.count_nonzero(ship == 1)
alien_probs[bot] = 0
crew_probs[bot] = 0

# Define the parameters
alpha = 0.5  # The probability of receiving a beep when a crew member is nearby
beta = 0.1  # The amount by which the probabilities are increased when a beep is received
k = 5  # The bot's detection range

# Run the game
for t in range(1000):  # Run for 100 timesteps
    # Update the crew member probabilities based on the bot's sensors
    # if np.random.rand() < alpha:  # The bot receives a beep
    #     crew_probs *= (1 + beta)
    # else:  # The bot does not receive a beep
    #     crew_probs *= (1 - alpha)
    # crew_probs /= crew_probs.sum()
    beep = np.random.rand() < alpha  # The bot receives a beep
    crew_probs = bayesian_update(crew_probs, beep, alpha, beta)

    # Update the alien probabilities based on the bot's sensors and the alien's movement
    alien_probs *= (1 - alpha)
    for dx in range(-k, k+1):
        for dy in range(-k, k+1):
            if 0 <= bot[0] + dx < ship.shape[0] and 0 <= bot[1] + dy < ship.shape[1]:
                alien_probs[bot[0] + dx, bot[1] + dy] = 1
    alien_probs /= alien_probs.sum()

    # Move the aliens
    for i in range(len(aliens)):
        old_position = aliens[i]
        aliens[i] = alien_bot_crew_movement.move_alien(aliens[i], ship)
        if aliens[i] != old_position:
            ship[old_position] = 1
            ship[aliens[i]] = 7

    # Print the current probabilities
    print(f"Time: {t}")
    print("Alien probabilities:")
    print(alien_probs)
    print("Crew member probabilities:")
    print(crew_probs)

    # Choose the next move
    possible_moves = [(bot[0] + dx, bot[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= bot[0] + dx < ship.shape[0] and 0 <= bot[1] + dy < ship.shape[1] and ship[bot[0] + dx, bot[1] + dy] == 1]
    if not possible_moves:
        print("No valid moves available. Ending game.")
        break

    # Choose the move with the highest crew member probability that is also safe
    safe_moves = [pos for pos in possible_moves if alien_probs[pos] == 0]
    if safe_moves:
        best_moves = sorted(safe_moves, key=lambda pos: crew_probs[pos], reverse=True)[:3]  # Get the top 3 safe moves
        best_move = best_moves[np.random.choice(len(best_moves))]  # Choose randomly from the top 3
    else:
        best_moves = sorted(possible_moves, key=lambda pos: crew_probs[pos] - alien_probs[pos], reverse=True)[:3]  # Get the top 3 moves
        best_move = best_moves[np.random.choice(len(best_moves))]  # Choose randomly from the top 3    

    # Move the bot
    old_position = bot
    bot = best_move
    if bot != old_position:
        ship[old_position] = 1
        ship[bot] = 5

    # Check if the bot saved a crew member or encountered an alien
    for crew_member in crew_members:
        if bot == crew_member:
            saves += 1
            print("Bot saved a crew member!")

    for alien in aliens:
        if bot == alien:
            failures += 1
            print("Bot encountered an alien!")

    # Print the current state
    print("Bot position:", bot)
    print("Alien position:", aliens[0])
    print("Crew member position:", crew_members[0])
    print()

    # Visualize the current state
    plt.figure(figsize=(10, 10))
    plt.imshow(ship, cmap='gray_r')
    plt.scatter([bot[1]], [bot[0]], color='blue')  # Bot is blue
    plt.scatter([alien[1] for alien in aliens], [alien[0] for alien in aliens], color='red')  # Aliens are red
    plt.scatter([crew_member[1] for crew_member in crew_members], [crew_member[0] for crew_member in crew_members], color='green')  # Crew members are green
    plt.title(f"Time: {t}")
    plt.show()

# Print the final counts
print("Number of saves:", saves)
print("Number of failures:", failures)