import numpy as np

def bayesian_update(probs, beep, alpha, beta, bot, old_position, k):
    """
    Update the probabilities based on whether a beep was received and the bot's movement.

    Parameters:
    probs (numpy.ndarray): The current probabilities.
    beep (bool): Whether a beep was received.
    alpha (float): The probability of receiving a beep when a crew member is nearby.
    beta (float): The amount by which the probabilities are increased when a beep is received.
    bot (tuple): The bot's current position.
    old_position (tuple): The bot's previous position.
    k (int): The detection range of the bot.

    Returns:
    numpy.ndarray: The updated probabilities.
    """
    for i in range(probs.shape[0]):
        for j in range(probs.shape[1]):
            if abs(i - bot[0]) <= k and abs(j - bot[1]) <= k:  # if cell is within detection range
                if beep:
                    update = alpha / (probs[i, j] * alpha + (1 - probs[i, j]) * beta)
                else:
                    update = (1 - alpha) / (probs[i, j] * (1 - alpha) + (1 - probs[i, j]) * (1 - beta))
                probs[i, j] *= update

    # Increase the probabilities if the bot is moving towards a crew member
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= bot[0] + dx < probs.shape[0] and 0 <= bot[1] + dy < probs.shape[1] and (bot[0] + dx, bot[1] + dy) == old_position:
            probs[bot[0] + dx, bot[1] + dy] *= 1.1  # Increase by 10%

    return probs

def move_bot(bot, alien_probs, crew_probs):
    # Combine the alien and crew member probabilities to get a total probability for each cell
    total_probs = alien_probs + crew_probs

    # Find the cell with the highest total probability
    max_prob_cell = np.unravel_index(total_probs.argmax(), total_probs.shape)

    # Move the bot to the cell with the highest total probability
    bot = max_prob_cell

    return bot