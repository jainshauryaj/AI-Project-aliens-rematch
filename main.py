import ship_generation
import alien_bot_crew_movement

# Generate a 50x50 ship
ship, time_taken = ship_generation.generate_ship(50)

# Print the generated ship and the time taken
print('\n')
print(ship)
print('\n')
print(f"Time taken: {time_taken} seconds")
print('\n')


bot, aliens, crew_members, ship = alien_bot_crew_movement.initialize_game(ship, k = 5, num_aliens = 6, num_crew = 1)

# Print the positions of the bot, aliens, and crew members
print("Bot position:", bot.position)

for i, alien in enumerate(aliens):
    print(f"Alien {i+1} position:", alien.position)

for i, crew_member in enumerate(crew_members):
    print(f"Crew member {i+1} position:", crew_member.position)
    
print('\n')
print(ship)