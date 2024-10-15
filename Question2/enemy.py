import pygame
import os
import random

class Enemy:
    def __init__(self, type, x, y, width, height, health, move_speed):
        # Initialize enemy attributes
        self.direction = 1
        self.x = x
        self.y = y - 10
        self.width = width + 13
        self.height = height + 13
        self.health = health
        self.vel = move_speed + 1
        self.type = type

        # Load animation images based on enemy type
        self.walk_right_animation_images = [pygame.image.load(os.path.join('images', f'enemy_walk_right_{i}.png')) for i in range(1, 8)]
        self.walk_left_animation_images = [pygame.transform.flip(image, True, False) for image in self.walk_right_animation_images]
        self.enemy_appear_images = [pygame.image.load(os.path.join('images', f'enemy_appear_{i}.png')) for i in range(1, 11)]
        self.fly_right_animation_images = [pygame.image.load(os.path.join('images', f'enemy_fly_{i}.png')) for i in range(1, 3)]
        self.fly_left_animation_images = [pygame.transform.flip(image, True, False) for image in self.fly_right_animation_images]
        self.boss_right_animation_images = [pygame.image.load(os.path.join('images', f'boss_{i}.png')) for i in range(1, 19)]
        self.boss_left_animation_images = [pygame.transform.flip(image, True, False) for image in self.boss_right_animation_images]

        # Initialize animation counters and speeds
        self.walk_animation_index = 0
        self.fly_animation_index = 0
        self.boss_animation_index = 0
        self.walk_animation_speed = 7
        self.fly_animation_speed = 5
        self.boss_animation_speed = 2
        self.walk_animation_counter = 0
        self.fly_animation_counter = 0
        self.boss_animation_counter = 0
        self.enemy_appear_speed = 3
        self.enemy_appear_index = 0
        self.enemy_appear_counter = 0

        # Initialize enemy appearance and state
        self.image = self.enemy_appear_images[self.enemy_appear_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.is_dead = False
        self.appear_done = False

    def update_direction(self, player_x):
        # Update enemy direction based on player position
        if self.x < player_x:
            self.direction = 1
        else:
            self.direction = -1

    def update_health(self, player, damage):
        # Update enemy health and check for death
        if self.type == 'boss':
            self.health -= damage/10
        elif self.type == 'walk':
            self.health -= damage/2
        else:
            self.health -= damage
        if self.health <= 0:
            self.die(player)

    def die(self, player):
        # Handle enemy death
        self.is_dead = True
        player.score += 10

    def appear(self):
        # Handle enemy appearance animation
        if not self.appear_done:
            self.image = self.enemy_appear_images[self.enemy_appear_index]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.enemy_appear_counter += 1
            if self.enemy_appear_counter % self.enemy_appear_speed == 0:
                self.enemy_appear_index = (self.enemy_appear_index + 1) % len(self.enemy_appear_images)
                if self.enemy_appear_index == 0:
                    self.appear_done = True

    def move(self, player_y):
        # Handle enemy movement based on type
        if self.type == 'walk':
            # Handle walking enemy movement
            if not self.is_dead and self.appear_done:
                self.x += self.vel * self.direction

                if self.direction == 1:
                    self.image = self.walk_right_animation_images[self.walk_animation_index]
                else:
                    self.image = self.walk_left_animation_images[self.walk_animation_index]

                self.image = pygame.transform.scale(self.image, (self.width, self.height))

                self.walk_animation_counter += 1
                if self.walk_animation_counter % self.walk_animation_speed == 0:
                    self.walk_animation_index = (self.walk_animation_index + 1) % len(self.walk_right_animation_images)
        elif self.type == 'fly':
            # Handle flying enemy movement
            if not self.is_dead:
                self.x += self.vel * self.direction
                if self.y < player_y:
                    self.y += self.vel/2
                elif self.y > player_y:
                    self.y -= self.vel/2

                if self.direction == -1:
                    self.image = self.fly_right_animation_images[self.fly_animation_index]
                else:
                    self.image = self.fly_left_animation_images[self.fly_animation_index]

                self.image = pygame.transform.scale(self.image, (self.width, self.height))

                self.fly_animation_counter += 1
                if self.fly_animation_counter % self.fly_animation_speed == 0:
                    self.fly_animation_index = (self.fly_animation_index + 1) % len(self.fly_right_animation_images)

        else:
            # Handle boss enemy movement
            if not self.is_dead:
                self.x += self.vel * self.direction
                if self.y < player_y:
                    self.y += self.vel/2
                elif self.y > player_y:
                    self.y -= self.vel/2

                if self.direction == -1:
                    self.image = self.boss_right_animation_images[self.boss_animation_index]
                else:
                    self.image = self.boss_left_animation_images[self.boss_animation_index]

                self.image = pygame.transform.scale(self.image, (self.width, self.height))

                self.boss_animation_counter += 1
                if self.boss_animation_counter % self.boss_animation_speed == 0:
                    self.boss_animation_index = (self.boss_animation_index + 1) % len(self.boss_right_animation_images)
