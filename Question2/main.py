import pygame
import os
from player import Player
from enemy import Enemy
from projectile import Projectile
from collectible import *
import random

pygame.init()

# Set up window dimensions
win_width, win_height = 640, 360
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Assignment 3 - Pygame - The Apocalypse")

# Load background image and extend the game world
bg_image = pygame.image.load(os.path.join('images', "background.png"))
bg_width = bg_image.get_width() * 3 # Extend the background to 3 times the window width
# Define variables for health bar dimensions
health_bar_width = 100
health_bar_height = 10

# Initialize display message timers and duration
display_message_timer_lv1 = 0
display_message_timer_lv2 = 0
display_message_timer_lv3 = 0
display_message_duration = 3

# Define current frame for animations
current_frame = 0

# Load images for player animations
run_animation_images = [pygame.image.load(os.path.join('images', f'running_{i}.png')) for i in range(1, 10)]
back_animation_images = [pygame.transform.flip(image, True, False) for image in run_animation_images]
jump_animation_images = [pygame.image.load(os.path.join('images', f'jump_{i}.png')) for i in range(1, 10)]
jump_back_animation_images = [pygame.transform.flip(image, True, False) for image in jump_animation_images]
idle_animation_images = [pygame.image.load(os.path.join('images', f'idle_{i}.png')) for i in range(1, 10)]
idle_left_animation_images = [pygame.transform.flip(image, True, False) for image in idle_animation_images]
shoot_animation_images = [pygame.image.load(os.path.join('images', f'shoot_{i}.png')) for i in range(1, 4)]
shoot_left_animation_images = [pygame.transform.flip(image, True, False) for image in shoot_animation_images]

# Create player object with animation images
player = Player(50, 250, 40, 60,
                run_animation_images, back_animation_images, jump_animation_images,
                jump_back_animation_images, idle_animation_images, idle_left_animation_images,
                shoot_animation_images, shoot_left_animation_images)

# Initialize list for projectiles
projectiles = []

# Load image for player lives
life_image = pygame.image.load(os.path.join('images', "lives.png"))
life_image = pygame.transform.scale(life_image, (37, 50))

# Initialize clock and frames per second
clock = pygame.time.Clock()
fps = 20

# Initialize list for enemies and variables for enemy spawning
enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = random.randint(30, 60)

# Define function to spawn enemies
def spawn_enemy(type):
    x = random.randint(50, win_width - 50)
    if type == 'walk':
        y = win_height - 90
    else: y = -20
    width = 35
    height = 35
    health = 50
    speed = random.uniform(1, 2)

    if type == 'walk':
        enemy = Enemy('walk', x, y, width, height, 30, speed)
    elif type == 'fly':
        enemy = Enemy('fly', x, y, width, height, 20, speed)
    else:
        enemy = Enemy('boss', x, y, 120, 100, 70, 2)
    enemies.append(enemy)

# Game loop
run = True
while run:
    # Display level up messages
    if (player.level == 1 and display_message_timer_lv1 <= display_message_duration * fps) \
            or (player.level == 2 and display_message_timer_lv2 <= display_message_duration * fps)\
            or (player.level == 3 and display_message_timer_lv3 <= display_message_duration * fps):
        # Display level up text
        font_large = pygame.font.Font(None, 72)
        if player.level == 1:
            level_up_text = font_large.render("LEVEL 1", True, (255, 255, 255))
        elif player.level == 2:
            level_up_text = font_large.render("LEVEL 2", True, (255, 255, 255))
        else:
            level_up_text = font_large.render("LEVEL 3", True, (255, 255, 255))
        text_rect = level_up_text.get_rect(center=(win_width // 2, win_height // 2))
        win.blit(level_up_text, text_rect)
        if player.level == 1:
            display_message_timer_lv1 += 1
        elif player.level == 2:
            display_message_timer_lv2 += 1
        else:
            display_message_timer_lv3 += 1
        pygame.display.update()

    # Control frame rate
    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

 # Calculate the camera offset
    camera_offset_x = 0
    if player.x > win_width // 2 and player.x < bg_width - win_width // 2:
        camera_offset_x = player.x - win_width // 2
    else:
        camera_offset_x = 0 if player.x <= win_width // 2 else bg_width - win_width

    win.blit(bg_image, (0 - camera_offset_x, 0))  # First background
    win.blit(bg_image, (bg_image.get_width() - camera_offset_x, 0))  # Second background
    win.blit(bg_image, (2 * bg_image.get_width() - camera_offset_x, 0))  # Third background


    # Handle player shooting
    if keys[pygame.K_SPACE] and player.can_shoot:
        direction = player.last_direction
        projectiles.append(Projectile(player.x + player.width // 2, player.y + player.height // 2, direction))
        player.can_shoot = False

    # Remove projectiles that are out of bounds
    projectiles = [projectile for projectile in projectiles if 0 < projectile.x < win_width]

    # Update and draw enemies
    for enemy in enemies:
        if not enemy.is_dead:
            enemy.update_direction(player.x + camera_offset_x)
            enemy.appear()
            enemy.move(player.y)
            if enemy.appear_done:
                if enemy.type == 'walk':
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x - camera_offset_x + 5, enemy.y - 10, 30, 5))
                    pygame.draw.rect(win, (255, 0, 0), (enemy.x - camera_offset_x + 5, enemy.y - 10, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x - camera_offset_x + 5, enemy.y - 10, max(0, enemy.health), 5))
                elif enemy.type == 'fly':
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x - camera_offset_x + 10, enemy.y, 20, 5))
                    pygame.draw.rect(win, (255, 0, 0), (enemy.x - camera_offset_x + 10 , enemy.y, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x - camera_offset_x + 10, enemy.y, max(0, enemy.health), 5))
                else:
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x - camera_offset_x + 30, enemy.y - 5, 70, 5))
                    pygame.draw.rect(win, (255, 0, 0), (enemy.x - camera_offset_x + 30, enemy.y - 5, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x - camera_offset_x + 30, enemy.y - 5, max(0, enemy.health), 5))

            win.blit(enemy.image, (enemy.x - camera_offset_x, enemy.y))

    # Handle collision between player and enemies
    for enemy in enemies:
        if (
                enemy.appear_done
                and not enemy.is_dead
                and player.x < enemy.x - camera_offset_x + enemy.width
                and player.x + player.width > enemy.x - camera_offset_x
                and player.y < enemy.y + enemy.height
                and player.y + player.height > enemy.y
        ):
            player.handle_collision(fps)

    # Update and draw projectiles
    for projectile in projectiles:
        if projectile.direction == 1:
            projectile.x += projectile.vel
        else:
            projectile.x -= projectile.vel
        projectile.update_image()
        win.blit(projectile.image, (projectile.x, projectile.y))

        # Check for collision between projectiles and enemies
        for enemy in enemies:
            if (
            enemy.appear_done
            and not enemy.is_dead
            and enemy.x - camera_offset_x < projectile.x < enemy.x - camera_offset_x + enemy.width
            and enemy.y < projectile.y < enemy.y + enemy.height
            ):
                enemy.update_health(player, 10)

                if projectile in projectiles:
                    projectiles.remove(projectile)

    # Update player
    player.update(win, win_width, keys)

    # Draw health bar for player
    pygame.draw.rect(win, (255, 0, 0), (10, 10, health_bar_width, health_bar_height))
    pygame.draw.rect(win, (0, 255, 0), (10, 10, player.health, health_bar_height))

    # Draw player lives
    for i in range(player.lives):
        win.blit(life_image, (win_width - 640 + i * 20, 10))

    # Increment enemy spawn timer and handle level transitions
    enemy_spawn_timer += 1
    if player.level == 1:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 15:
                spawn_enemy('walk')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(30, 60)

            if len(enemies) > 0 and all(enemy.appear_done and enemy.is_dead for enemy in enemies):
                player.level = 2
                enemies.clear()

    if player.level == 2:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 20:
                spawn_enemy('fly')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(30, 60)

            if len(enemies) > 0 and all(enemy.appear_done and enemy.is_dead for enemy in enemies):
                player.level = 3
                enemies.clear()

    if player.level == 3 and not player.win:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 15:
                spawn_enemy('walk')
                spawn_enemy('fly')
                spawn_enemy('fly')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(50, 100)

            if not player.win and len(enemies) > 0 and all(enemy.appear_done and enemy.type != 'boss' and enemy.is_dead for enemy in enemies):
                spawn_enemy('boss')

            if not player.win and any(enemy.type == 'boss' and enemy.is_dead for enemy in enemies):
                player.win = True
                enemies.clear()

    # Spawn and handle collectibles
    spawn_collectible(player)
    update_and_draw_collectibles(win, player,camera_offset_x)
    handle_collectible_collision(player)

    # Display score and level information
    font = pygame.font.SysFont(None,25)
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))

    win.blit(score_text, (550, 10))
    win.blit(level_text, (550, 40))

    # Display game over/win screen
    if player.lives <= 0 or player.win:
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        if not player.win:
            final_text = font.render("DEFEAT", True, (255, 0, 0))
        else:
            final_text = font.render("VICTORY", True, (255, 0, 0))
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        prompt_text = font.render("Play again? (Y/N)", True, (255, 255, 255))
        win.blit(final_text,
                 (win_width // 2 - final_text.get_width() // 2, win_height // 2 - final_text.get_height() // 2))
        win.blit(score_text, (win_width // 2 - score_text.get_width() // 2, win_height // 2 + 50))
        win.blit(prompt_text, (win_width // 2 - prompt_text.get_width() // 2, win_height // 2 + 100))

        # Handle player input for playing again
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            # Reset game state and restart the game
            player.reset(enemies)  # Implement reset() method in Player class to reset player state
            # Reset enemies, score, etc.
        elif keys[pygame.K_n]:
            run = False  # Quit the game if the player doesn't want to play again

    pygame.display.update()

pygame.quit()
