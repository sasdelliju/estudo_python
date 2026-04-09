import pygame
import random
import sys

pygame.init()

WIDTH = 700
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Deluxe")

WHITE = (255, 255, 255)
BLACK = (5, 5, 20)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

# -------- ESTRELAS --------
stars = []
for _ in range(80):
    stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1,3)])

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        star[1] += star[2]  # velocidade proporcional ao tamanho
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

# -------- EXPLOSÃO --------
class Explosion:
    def __init__(self, x, y):
        self.sprite_sheet = pygame.image.load("explosion.jpg").convert_alpha()

        self.rows = 5
        self.cols = 5
        self.total_frames = self.rows * self.cols

        self.frame_width = self.sprite_sheet.get_width() // self.cols
        self.frame_height = self.sprite_sheet.get_height() // self.rows

        self.frames = []
        for row in range(self.rows):
            for col in range(self.cols):
                frame = self.sprite_sheet.subsurface(
                    col * self.frame_width,
                    row * self.frame_height,
                    self.frame_width,
                    self.frame_height
                )
                self.frames.append(frame)

        self.current_frame = 0
        self.animation_speed = 2  # menor = mais rápido
        self.counter = 0
        self.x = x
        self.y = y

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.current_frame += 1

    def draw(self):
        if self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            rect = frame.get_rect(center=(self.x, self.y))
            screen.blit(frame, rect)

    def finished(self):
        return self.current_frame >= len(self.frames)

def reset_game():
    global player_x, player_lives, bullet, enemies
    global enemy_direction, enemy_speed, explosions, score, enemy_bullets

    player_x = WIDTH // 2 - 30
    player_lives = 3
    bullet = None
    score = 0

    enemies = []
    for row in range(4):
        for col in range(8):
            enemies.append(pygame.Rect(80 + col * 70, 60 + row * 50, 40, 25))

    enemy_direction = 1
    enemy_speed = 1   # 🔥 MAIS LENTO
    enemy_bullets = []
    explosions = []

reset_game()

player_y = HEIGHT - 50
player_speed = 6
bullet_speed = 8
enemy_bullet_speed = 3   # 🔥 tiros inimigos mais lentos

running = True
game_over = False

while running:
    clock.tick(120)
    screen.fill(BLACK)

    draw_stars()  # 🌌 fundo animado

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE and bullet is None:
                    bullet = pygame.Rect(player_x + 25, player_y, 5, 12)
            else:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 60:
            player_x += player_speed

    player = pygame.Rect(player_x, player_y, 60, 15)
    pygame.draw.rect(screen, GREEN, player)

    # -------- MOVIMENTO CLÁSSICO --------
    move_down = False

    for enemy in enemies:
        enemy.x += enemy_direction * enemy_speed
        if enemy.right >= WIDTH - 20 or enemy.left <= 20:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 10

    # -------- TIRO PLAYER --------
    if bullet:
        bullet.y -= bullet_speed
        pygame.draw.rect(screen, WHITE, bullet)

        if bullet.y < 0:
            bullet = None

        for enemy in enemies[:]:
            if bullet and bullet.colliderect(enemy):
                explosions.append(Explosion(enemy.centerx, enemy.centery))
                enemies.remove(enemy)
                bullet = None
                score += 10

    # -------- TIROS INIMIGOS --------
    if random.randint(0, 80) == 1 and enemies:
        shooter = random.choice(enemies)
        enemy_bullets.append(pygame.Rect(shooter.centerx, shooter.bottom, 5, 12))

    for eb in enemy_bullets[:]:
        eb.y += enemy_bullet_speed
        pygame.draw.rect(screen, RED, eb)

        if eb.colliderect(player):
            enemy_bullets.remove(eb)
            player_lives -= 1
            if player_lives <= 0:
                game_over = True

        elif eb.y > HEIGHT:
            enemy_bullets.remove(eb)

    # -------- DESENHAR INIMIGOS --------
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
        if enemy.bottom >= player_y:
            game_over = True

    # -------- EXPLOSÕES --------
    for explosion in explosions[:]:
        explosion.update()
        explosion.draw()
        if explosion.finished():
            explosions.remove(explosion)

    # -------- HUD --------
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        restart_text = font.render("Pressione R para reiniciar", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - 180, HEIGHT//2 - 40))
        screen.blit(restart_text, (WIDTH//2 - 160, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
