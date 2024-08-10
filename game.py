import pygame
import sys
import random
import os

pygame.init()

width = 330
height = 600
background_image = pygame.image.load("imagens/space.jpg")

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BATTLESHIP")
clock = pygame.time.Clock()

player_image = pygame.image.load("imagens/player.png")
player_rect = player_image.get_rect()
player_rect.centerx = width // 2
player_rect.bottom = height - 10

enemy_image = pygame.image.load("imagens/enemy.png")
enemy_size = enemy_image.get_rect().size
enemies = []

score = 0
font = pygame.font.Font(None, 36)

def spawn_enemy():
    enemy_rect = enemy_image.get_rect()
    enemy_rect.x = random.randint(0, width - enemy_size[0])
    enemy_rect.y = -enemy_size[1]
    enemies.append(enemy_rect)

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def save_score(score):
    scores = []
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            for line in file:
                try:
                    scores.append(int(line.strip()))
                except ValueError:
                    continue
    
    scores.append(score)
    scores = sorted(scores, reverse=True)[:3]
    
    with open("scores.txt", "w") as file:
        for s in scores:
            file.write(f"{s}\n")
    print("Pontuação salva!")

def show_menu():
    while True:
        screen.blit(background_image, (0, 0))
        title_font = pygame.font.Font(None, 50)
        menu_font = pygame.font.Font(None, 36)

        title_text = title_font.render("BATTLESHIP", True, (0, 0, 0))
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))

        start_text = menu_font.render("1. Start Game", True, (0, 0, 0))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - 100))

        score_text = menu_font.render("2. Score Record", True, (0, 0, 0))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - 50))

        exit_text = menu_font.render("3. Exit", True, (0, 0, 0))
        screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'start'
                elif event.key == pygame.K_2:
                    return 'score'
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def show_scores():
    screen.blit(background_image, (0, 0))
    title_font = pygame.font.Font(None, 60)
    score_font = pygame.font.Font(None, 36)
    
    title_text = title_font.render("High Scores", True, (0, 0, 0))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4 - 50))

    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            scores = [line.strip() for line in file]
            scores = scores[:3]
    else:
        scores = ["No scores recorded yet."]
    
    y = height // 2 - 50
    for i, score in enumerate(scores):
        score_text = score_font.render(f"{i + 1}. {score}", True, (0, 0, 0))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, y))
        y += 40
    
    pygame.display.flip()
    pygame.time.wait(3000)

def choose_difficulty():
    global enemy_speed
    global enemy_spawn_interval

    while True:
        screen.blit(background_image, (0, 0))
        title_font = pygame.font.Font(None, 50)
        menu_font = pygame.font.Font(None, 36)

        title_text = title_font.render("Choose Difficulty", True, (0, 0, 0))
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))

        easy_text = menu_font.render("1. Easy", True, (0, 0, 0))
        screen.blit(easy_text, (width // 2 - easy_text.get_width() // 2, height // 2 - 50))

        medium_text = menu_font.render("2. Medium", True, (0, 0, 0))
        screen.blit(medium_text, (width // 2 - medium_text.get_width() // 2, height // 2))

        hard_text = menu_font.render("3. Hard", True, (0, 0, 0))
        screen.blit(hard_text, (width // 2 - hard_text.get_width() // 2, height // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    enemy_speed = 2
                    enemy_spawn_interval = 2000
                    return
                elif event.key == pygame.K_2:
                    enemy_speed = 3
                    enemy_spawn_interval = 1500
                    return
                elif event.key == pygame.K_3:
                    enemy_speed = 4
                    enemy_spawn_interval = 1000
                    return
                

def game_loop():
    global score
    global enemy_speed
    global enemy_spawn_interval

    score = 0
    running = True
    spawn_time = pygame.time.get_ticks()
    
    choose_difficulty()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5
        
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > width:
            player_rect.right = width
        
        for enemy_rect in enemies[:]:
            enemy_rect.y += enemy_speed
            if enemy_rect.top > height:
                enemies.remove(enemy_rect)
                score += 1
            if enemy_rect.colliderect(player_rect):
                print("Game Over!")
                running = False
        
        current_time = pygame.time.get_ticks()
        if current_time - spawn_time > enemy_spawn_interval:
            spawn_enemy()
            spawn_time = current_time
        
        screen.blit(background_image, (0, 0))
        screen.blit(player_image, player_rect)
        for enemy_rect in enemies:
            screen.blit(enemy_image, enemy_rect)
        draw_score()
        pygame.display.flip()

        clock.tick(60)

    save_score(score)
    show_menu()

def main():
    while True:
        choice = show_menu()
        if choice == 'start':
            game_loop()
        elif choice == 'score':
            show_scores()

if __name__ == '__main__':
    main()
