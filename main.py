import pygame
import random

from space.constants_game import ConstantGame
from space.laser import collide
from space.class_ship import Player, Enemy, Reward

pygame.font.init()

def draw_lives(win, lives):
    lives_label = ConstantGame.main_font.render(f"Lives: {lives}", 1, ConstantGame.WHITE)
    win.blit(lives_label, (10, 10))

def draw_level(win, level):
    level_label = ConstantGame.main_font.render(f"Level: {level}", 1, ConstantGame.WHITE)
    win.blit(level_label, (ConstantGame.WIDTH - level_label.get_width() - 10, 10))

def draw_lost(win):
    lost_label = ConstantGame.lost_font.render("You Lost!!", 1, ConstantGame.WHITE)
    win.blit(lost_label, (ConstantGame.WIDTH/2 - lost_label.get_width()/2, 350))

def main():
    pygame.init()

    ConstantGame.WIN = pygame.display.set_mode((ConstantGame.WIDTH, ConstantGame.HEIGHT))
    pygame.display.set_caption("Space Invaders")

    ConstantGame.BG = ConstantGame.make_background()
    ConstantGame.main_font = pygame.font.SysFont("comicsans", 35)
    ConstantGame.lost_font = pygame.font.SysFont("comicsans", 55)

    clock = pygame.time.Clock()

    run = True
    level = 0
    lives = 5

    enemies = []
    rewards = []

    wave_length = 5
    enemy_vel = ConstantGame.ENEMY_VEL
    reward_vel = ConstantGame.REWARD_VEL
    player_vel = ConstantGame.PLAYER_VEL
    laser_vel = ConstantGame.LASER_VEL

    player = Player(250, 630)

    lost = False
    lost_count = 0

    reward_timer = 0

    def redraw_window():
        ConstantGame.WIN.blit(ConstantGame.BG, (0, 0))
        draw_lives(ConstantGame.WIN, lives)
        draw_level(ConstantGame.WIN, level)

        for enemy in enemies:
            enemy.draw(ConstantGame.WIN)

        for reward in rewards:
            reward.draw(ConstantGame.WIN)

        player.draw(ConstantGame.WIN)

        if lost:
            draw_lost(ConstantGame.WIN)

        pygame.display.update()

    while run:
        clock.tick(ConstantGame.FPS)
        reward_timer += 1

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > ConstantGame.FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, ConstantGame.WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"])
                )
                enemies.append(enemy)

        if reward_timer >= ConstantGame.REWARD_SPAWN_TICKS:
            reward = Reward(
                random.randrange(50, ConstantGame.WIDTH - 50),
                random.randrange(-1500, -100),
            )
            rewards.append(reward)
            reward_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < ConstantGame.WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < ConstantGame.HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if random.randrange(0, 2 * ConstantGame.FPS) == 1:
                enemy.shoot()

            enemy.move_lasers(laser_vel, [player])

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > ConstantGame.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        for reward in rewards[:]:
            reward.move(reward_vel)

            if reward.off_screen(ConstantGame.HEIGHT):
                rewards.remove(reward)
            elif reward.collision(player):
                player.health = min(player.max_health, player.health + ConstantGame.REWARD_HEAL)
                rewards.remove(reward)

        player.move_lasers(-laser_vel, enemies)

    pygame.quit()

def main_menu():
    pygame.init()
    ConstantGame.WIN = pygame.display.set_mode((ConstantGame.WIDTH, ConstantGame.HEIGHT))
    pygame.display.set_caption("Space Invaders")
    ConstantGame.BG = ConstantGame.make_background()
    ConstantGame.main_font = pygame.font.SysFont("comicsans", 35)
    title_font = pygame.font.SysFont("comicsans", 45)

    run = True
    while run:
        ConstantGame.WIN.blit(ConstantGame.BG, (0, 0))

        title_label = title_font.render("Press the mouse to begin...", 1, ConstantGame.WHITE)
        ConstantGame.WIN.blit(title_label, (ConstantGame.WIDTH/2 - title_label.get_width()/2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
