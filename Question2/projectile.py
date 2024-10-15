import pygame
import os

class Projectile:
    def __init__(self, x, y, direction):
        # Initialize projectile attributes
        self.x = x
        self.y = y - 8  # Adjust y position for projectile origin
        self.direction = 1  # Default direction
        self.vel = 7 * direction  # Velocity based on direction
        self.width = 17
        self.height = 17
        # Load projectile images
        self.images = [pygame.image.load(os.path.join('images', f'bullet_{i}.png')) for i in range(1, 6)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update_image(self):
        # Update projectile image for animation
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
