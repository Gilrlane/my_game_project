import pygame
import random
import time
import os

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dalek Defense")

# Cores
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
gray = (100, 100, 100)

# Função para carregar e redimensionar imagens
def load_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

# Carregar e redimensionar imagens (Certifique-se de que os caminhos estão corretos)
background = load_image('assets/background.png', screen_width, screen_height)
tower_img = load_image('assets/tower.png', 100, 100)
enemy_img = load_image('assets/enemy.png', 40, 40)
bullet_img = load_image('assets/bullet.png', 16, 16)

# Funções para desenhar os elementos do jogo
def draw_tower(x, y):
    screen.blit(tower_img, (x, y))

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    screen.blit(bullet_img, (x, y))

def display_message(msg, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    screen.blit(text, (x, y))

# Função para salvar o score
def save_score(score):
    with open('scores.txt', 'a') as file:
        file.write(f"{score}\n")

# Função para obter os top 5 scores
def get_top_scores():
    if not os.path.exists('scores.txt'):
        return []
    with open('scores.txt', 'r') as file:
        scores = file.readlines()
    scores = [int(score.strip()) for score in scores if score.strip().isdigit()]
    scores.sort(reverse=True)
    return scores[:5]

# Função para desenhar o botão
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, active_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, button_rect)

    display_message(text, black, 30, x + 10, y + 10)

# Função para reiniciar o jogo
def restart_game():
    global tower_x, tower_y, tower_speed, enemy_speed, enemy_x, enemy_y
    global bullet_speed, bullet_x, bullet_y, bullet_state, score
    global start_time, game_state

    # Resetar variáveis do jogo
    tower_x = screen_width // 2
    tower_y = screen_height - 70
    tower_speed = 10

    enemy_speed = 2
    enemy_x = random.randint(0, screen_width - 64)
    enemy_y = -64

    bullet_speed = 10
    bullet_x = -10
    bullet_y = tower_y
    bullet_state = "ready"

    score = 0

    start_time = time.time()
    game_state = 'playing'

# Inicialização das variáveis do jogo
tower_x = screen_width // 2
tower_y = screen_height - 70
tower_speed = 10
defense_line_y = tower_y - 50

enemy_speed = 2
enemy_x = random.randint(0, screen_width - 64)
enemy_y = -64

bullet_speed = 10
bullet_x = -10
bullet_y = tower_y
bullet_state = "ready"

score = 0

# Definindo o tempo de jogo 
game_duration = 60  # segundos
start_time = time.time()  # Tempo inicial do jogo

# Função para verificar colisão entre dois objetos
def is_collision(obj1_x, obj1_y, obj2_x, obj2_y, obj_size):
    return (obj1_x < obj2_x + obj_size and
            obj1_x + obj_size > obj2_x and
            obj1_y < obj2_y + obj_size and
            obj1_y + obj_size > obj2_y)

# Função para verificar se o inimigo atingiu a linha de defesa
def check_defense_line(enemy):
    x, y = enemy
    if y > defense_line_y:
        return True
    return False

# Função para remover inimigo da lista
def remove_enemy(enemy):
    enemies.remove(enemy)

# Estado inicial do jogo
game_state = 'playing'

# Loop principal do jogo
running = True
while running:
    screen.fill(white)
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == 'playing':
        # Calculando o tempo restante
        elapsed_time = time.time() - start_time
        time_left = game_duration - elapsed_time
        
        if time_left <= 0:
            game_state = 'game_over'
            save_score(score)
        
        # Movimentação da torre com as teclas de seta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tower_x -= tower_speed
        if keys[pygame.K_RIGHT]:
            tower_x += tower_speed
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_x = tower_x + 32
            bullet_y = tower_y
            bullet_state = "fire"
        
        # Atualização da posição da torre
        if tower_x <= 0:
            tower_x = 0
        elif tower_x >= screen_width - 64:
            tower_x = screen_width - 64
        
        # Atualização do inimigo
        enemy_y += enemy_speed
        
        # Verificar se o inimigo atingiu a linha de defesa
        if check_defense_line((enemy_x, enemy_y)):
            score -= 10
            enemy_y = -64
            enemy_x = random.randint(0, screen_width - 64)
        
        # Verificar se o inimigo saiu da tela e não atingiu a linha de defesa
        if enemy_y > screen_height:
            enemy_y = -64
            enemy_x = random.randint(0, screen_width - 64)
        
        # Atualização do projétil
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_speed
        
        if bullet_y <= 0:
            bullet_y = tower_y
            bullet_state = "ready"
        
        # Verificar colisão do projétil com o inimigo
        if is_collision(bullet_x, bullet_y, enemy_x, enemy_y, 64):
            enemy_y = -64
            enemy_x = random.randint(0, screen_width - 64)
            bullet_y = tower_y
            bullet_state = "ready"
            score += 10  
        
        # Desenhar elementos
        draw_tower(tower_x, tower_y)
        draw_enemy(enemy_x, enemy_y)
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
        
        # Exibir o score e o tempo restante
        display_message(f"Score: {score}", red, 30, 10, 10)
        display_message(f"Time Left: {int(time_left)}s", red, 30, screen_width - 200, 10)
    
    elif game_state == 'game_over':
        # Obter os top 5 scores
        top_scores = get_top_scores()
        
        # Exibir mensagem de game over
        display_message("Fantástico!", red, 50, screen_width // 2 - 150, screen_height // 2 - 150)
        display_message(f"Final Score: {score}", red, 40, screen_width // 2 - 120, screen_height // 2 - 80)
        
        # Exibir os top 5 scores
        display_message("Top 5 Scores:", black, 40, screen_width // 2 - 100, screen_height // 2 - 20)
        for idx, top_score in enumerate(top_scores):
            display_message(f"{idx + 1}. {top_score}", black, 30, screen_width // 2 - 50, screen_height // 2 + 20 + idx * 40)
        
        # Desenhar o botão "Jogar Novamente"
        draw_button("Jogar Novamente", screen_width // 2 - 100, screen_height // 2 + 220, 200, 50, green, gray, restart_game)
    
    pygame.display.update()

pygame.quit()
