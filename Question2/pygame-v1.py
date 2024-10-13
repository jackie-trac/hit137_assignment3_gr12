#IMPORTS
import pygame
import math
import sys
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, K_x, K_LSHIFT, K_SPACE, KEYDOWN, KEYUP, QUIT
)

pygame.init()

# SCREEN; GRAVITY
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1

# IMAGES
def load_image(path):
    img = pygame.image.load('Sprites/' + path)
    img.set_colorkey((0, 0, 0))
    return img

def animation(list, pos):
    return list[pos % len(list)]

# PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.faced_left = True
        self.shoot = False
        self.sprinting = False
        self.jumping = False
        self.velocity_y = 0
        self.f = 0
        self.speed = 5
        self.jump_speed = -15
        self.image = Still
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.health = 100
        self.lives = 3 

    def update(self):
        current_speed = self.speed * 2 if self.sprinting else self.speed
        if self.up:
            self.f += 0.25
            self.image = animation(Climb, math.floor(self.f))
            self.rect.move_ip(0, -current_speed)
        elif self.down:
            self.f += 0.25
            self.image = animation(Climb, math.floor(self.f))
            self.rect.move_ip(0, current_speed)
        else:
            if self.shoot:
                self.image = gunL if self.faced_left else gunR
            elif self.left and not self.right:
                self.f += 0.25
                self.image = animation(Lwalk, math.floor(self.f))
                self.rect.move_ip(-current_speed, 0)
            elif self.right and not self.left:
                self.f += 0.25
                self.image = animation(Rwalk, math.floor(self.f))
                self.rect.move_ip(current_speed, 0)
            else:
                self.f = 0
                self.image = Still

        # JUMP FUNCTION
        if self.jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += GRAVITY
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.jumping = False
                self.velocity_y = 0

    def draw_health_bar(self, surface):
        bar_length = 100
        bar_height = 10
        fill = (self.health / 100) * bar_length
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_length, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

    def draw_lives(self, surface):
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        surface.blit(lives_text, (10, 10))

# PROJECTILE CLASS
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage):
        super().__init__()
        self.image = load_image('Projectile.png') 
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.damage = damage

    def update(self):
        if self.direction == 'left':
            self.rect.x -= 10
        elif self.direction == 'right':
            self.rect.x += 10
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# ENEMY CLASS
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('Enemy.png')  # JERICHO: @Lachlan, we will need sprite for the enemy.
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.health = 50 

    def update(self):
        # Simple left-to-right movement
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.speed = -self.speed

    def draw_health_bar(self, surface):
        bar_length = 50
        bar_height = 5
        fill = (self.health / 50) * bar_length
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_length, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

# SPRITES
Still = load_image('Standing.png')
gunL = load_image('Lgun.png')
gunR = load_image('Rgun.png')
Lwalk = [load_image('LW1.png'), load_image('LW2.png'), load_image('LW3.png'), load_image('LW4.png')]
Rwalk = [load_image('RW1.png'), load_image('RW2.png'), load_image('RW3.png'), load_image('RW4.png')]
Climb = [load_image('Climb1.png'), load_image('Climb2.png')]

# MAIN LOOP
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# ENEMIES
for i in range(5):
    enemy = Enemy(x=100 * i, y=100)
    all_sprites.add(enemy)
    enemies.add(enemy)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def quit_game():
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_game()
            elif event.key == K_UP:
                player.up = True
            elif event.key == K_DOWN:
                player.down = True
            elif event.key == K_LEFT:
                player.left = True
                player.faced_left = True
            elif event.key == K_RIGHT:
                player.right = True
                player.faced_left = False
            elif event.key == K_x:
                player.shoot = True
                direction = 'left' if player.faced_left else 'right'
                projectile = Projectile(player.rect.centerx, player.rect.centery, direction, damage=10)
                all_sprites.add(projectile)
                projectiles.add(projectile)
            elif event.key == K_LSHIFT:
                player.sprinting = True
            elif event.key == K_SPACE and not player.jumping: 
                player.jumping = True
                player.velocity_y = player.jump_speed
        elif event.type == KEYUP:
            if event.key == K_UP:
                player.up = False
            if event.key == K_DOWN:
                player.down = False
            if event.key == K_LEFT:
                player.left = False
            if event.key == K_RIGHT:
                player.right = False
            if event.key == K_x:
                player.shoot = False
            if event.key == K_LSHIFT:
                player.sprinting = False
        elif event.type == QUIT:
            quit_game()

    screen.fill((100, 100, 100))
    all_sprites.update()

    # COLLISSION CHECK between projectiles and enemies
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for hit in hits:
        enemy = hits[hit][0]
        enemy.health -= hit.damage
        if enemy.health <= 0:
            enemy.kill()

    for entity in all_sprites:
        if isinstance(entity, Projectile):
            screen.blit(entity.image, entity.rect)
        else:
            screen.blit(entity.image, entity.rect)
            if isinstance(entity, Player):
                entity.draw_health_bar(screen)
                entity.draw_lives(screen)
            elif isinstance(entity, Enemy):
                entity.draw_health_bar(screen)

    pygame.display.flip()
    clock.tick(30)
