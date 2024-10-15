import pygame
import random
import os

class Collectible:
    def __init__(self, x, image):
        self.x = x
        self.y = -50  # Start from the top of the screen
        self.image = image
        self.velocity = 2  # Velocity of the collectible falling down
        self.is_active = True  # Determine if the collectible is active or not

    def update(self):
        # If the collectible is not active, do not update its position
        if not self.is_active:
            return

        # Update the position of the collectible
        self.y += self.velocity

        # Check if the collectible has fallen off the screen
        if self.y > screen_height:
            # Deactivate the collectible
            self.is_active = False

    def check_collision(self, player):
        # Check collision with the player
        if (
            self.is_active
            and self.x < player.x + player.width
            and self.x + self.image.get_width() > player.x
            and self.y < player.y + player.height
            and self.y + self.image.get_height() > player.y
        ):
            # Determine the type of collectible
            if self.image == extra_life_image:
                player.lives += 1
                player.score += 10
            elif self.image == health_boost_image:
                player.health += 20
                if player.health > 100:
                    player.health = 100  # Increase player's health but cap it at 100
                player.score += 10

            # Deactivate the collectible
            self.is_active = False

    def reset(self):
        # Reset the position and state of the collectible
        self.y = -50
        self.is_active = True

def spawn_collectible(player):
    global collectibles

    # The position on the x-axis
    x = 300

    # Randomly choose the type of collectible (health_boost or extra_life)
    if len(collectibles) == 0:
        if player.score > 0 and player.score % 100 == 0:
            collectible = Collectible(x, health_boost_image)
            collectibles.append(collectible)

        if player.level == 3 and player.extra_life == False:
            collectible = Collectible(x, extra_life_image)
            collectibles.append(collectible)
            player.extra_life = True

# Screen dimensions
screen_width = 800
screen_height = 600

# Load collectible images and resize them
health_boost_image = pygame.image.load(os.path.join('images', 'health.png'))
health_boost_image = pygame.transform.scale(health_boost_image, (20, 30))  # Resize here

extra_life_image = pygame.image.load(os.path.join('images', 'life.png'))
extra_life_image = pygame.transform.scale(extra_life_image, (20, 30))  # Resize here

# List of collectibles
collectibles = []

# Function to handle collision between the player and collectibles
def handle_collectible_collision(player):
    for collectible in collectibles:
        collectible.check_collision(player)

# Function to update and draw all collectibles
def update_and_draw_collectibles(screen, player, camera_offset_x):
    global collectibles
    for collectible in collectibles:
        collectible.update()
        # Draw the collectible relative to the camera offset
        screen.blit(collectible.image, (collectible.x - camera_offset_x, collectible.y))
    # Remove inactive collectibles
    collectibles = [collectible for collectible in collectibles if collectible.is_active]

# Function to reset all collectibles
def reset_collectibles():
    global collectibles
    for collectible in collectibles:
        collectible.reset()
