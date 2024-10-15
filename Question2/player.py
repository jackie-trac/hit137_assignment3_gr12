import pygame
import os

class Player:
    def __init__(self, x, y, width, height, run_animation_images, back_animation_images, jump_animation_images,
                 jump_back_animation_images, idle_animation_images, idle_left_animation_images,
                 shoot_animation_images, shoot_left_animation_images):
        self.idle_right_animation_images = [pygame.image.load(os.path.join('images', f'idle_{i}.png')) for i in
                                           range(1, 10)]
        self.idle_left_animation_images = [pygame.transform.flip(image, True, False) for image in self.idle_right_animation_images]
        self.last_direction = 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.isJump = False
        self.jumpCount = 10
        self.can_shoot = True
        self.health = 100
        self.lives = 3
        self.collision_timer = 0
        self.collision_cooldown = 0.5
        self.collision_cooldown_timer = 0
        self.current_frame = 0

        # Animation images
        self.run_animation_images = run_animation_images
        self.back_animation_images = back_animation_images
        self.jump_animation_images = jump_animation_images
        self.jump_back_animation_images = jump_back_animation_images
        self.idle_animation_images = idle_animation_images
        self.idle_left_animation_images = idle_left_animation_images
        self.shoot_animation_images = shoot_animation_images
        self.shoot_left_animation_images = shoot_left_animation_images

        self.level = 1
        self.score = 0
        self.extra_life = False
        self.win = False

    # Method to handle collision with enemies
    def handle_collision(self, fps):
        if self.collision_timer <= 0:
            self.update_health(10)
            self.collision_timer = 0.5
        else:
            self.collision_timer -= 1 / fps

    # Method to move the player left
    def move_left(self):
        self.x -= self.vel

    # Method to move the player right
    def move_right(self, win_width):
        self.x += self.vel
        if self.x > win_width - self.width:
            self.x = win_width - self.width

    def jump(self):
        if not self.isJump:
            self.isJump = True

    # Method to make the player jump
    def handle_jump(self):
        if self.jumpCount >= -10:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
            self.y -= (self.jumpCount ** 2) * 0.3 * neg
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 10

    def update_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = 100

    # Method to update player's animation and handle player's movement
    def update_animation(self, win, win_width, keys):
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.move_left()

        if keys[pygame.K_RIGHT]:
            self.move_right(win_width)

        if keys[pygame.K_UP]:
            self.jump()

        if self.isJump:
            self.handle_jump()

        if keys[pygame.K_RIGHT] and not self.isJump:
            self.last_direction = 1
            if keys[pygame.K_SPACE]:
                self.current_frame = (self.current_frame + 1) % len(self.shoot_animation_images)
                win.blit(self.shoot_animation_images[self.current_frame], (self.x, self.y))
            else:
                win.blit(self.run_animation_images[self.current_frame], (self.x, self.y))
        elif keys[pygame.K_LEFT] and not self.isJump:
            self.last_direction = -1
            if keys[pygame.K_SPACE]:
                self.current_frame = (self.current_frame) % len(self.shoot_left_animation_images)
                win.blit(self.shoot_left_animation_images[self.current_frame], (self.x, self.y))
            else:
                win.blit(self.back_animation_images[self.current_frame], (self.x, self.y))
        elif keys[pygame.K_RIGHT] and self.isJump:
            self.last_direction = 1
            win.blit(self.jump_animation_images[self.current_frame], (self.x, self.y))
        elif keys[pygame.K_LEFT] and self.isJump:
            self.last_direction = -1
            win.blit(self.jump_back_animation_images[self.current_frame], (self.x, self.y))
        elif self.isJump:
            if self.last_direction == 1:
                win.blit(self.jump_animation_images[self.current_frame], (self.x, self.y))
            else:
                win.blit(self.jump_back_animation_images[self.current_frame], (self.x, self.y))
        else:
            if keys[pygame.K_SPACE]:
                self.current_frame = (self.current_frame + 1) % len(self.shoot_animation_images)
                if self.last_direction == 1:
                    win.blit(self.shoot_animation_images[self.current_frame], (self.x, self.y))
                else:
                    win.blit(self.shoot_left_animation_images[self.current_frame], (self.x, self.y))
            elif self.last_direction == 1:
                win.blit(self.idle_animation_images[self.current_frame], (self.x, self.y))
            else:
                win.blit(self.idle_left_animation_images[self.current_frame], (self.x, self.y))

        self.current_frame = (self.current_frame + 1) % 9

    # Method to update player's state
    def update(self, win, win_width, keys):
        self.update_animation(win, win_width, keys)  # Update player's animation and movement

        if not keys[pygame.K_SPACE]:
            self.can_shoot = True  # Set player's ability to shoot

    # Method to reset player's state
    def reset(self, enemies):
        # Reset all player attributes to their initial values
        self.x = 50
        self.y = 250
        self.health = 100
        self.lives = 3
        self.level = 1
        self.score = 0
        self.win = False
        enemies.clear()