import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, 300
BIRD_RADIUS = 20
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -8
SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
bird_image = pygame.image.load("bird1.png")
bird_image = pygame.transform.scale(bird_image, (40, 30))
background = pygame.image.load("background12.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, HEIGHT))
flap_sound = pygame.mixer.Sound("wing-flap-1-6434.mp3")
point_sound = pygame.mixer.Sound("point-smooth-beep-230573.mp3")
hit_sound = pygame.mixer.Sound("orchestra-hit-240475.mp3")

# Load high score
score_file = "highscore.txt"
def load_high_score():
    if os.path.exists(score_file):
        with open(score_file, "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open(score_file, "w") as file:
        file.write(str(score))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bamboo in the Sky")

def draw_button(text, x, y, width, height, action=None):
    font = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, rect, border_radius=10)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 10))
    return rect

# Main Menu Function
def main_menu():
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        font = pygame.font.SysFont(None, 40)
        title = font.render("Flappy Bird", True, BLACK)
        high_score_text = font.render(f"High Score: {load_high_score()}", True, BLACK)
        screen.blit(title, (120, 100))
        screen.blit(high_score_text, (120, 180))

        start_button = draw_button("Start Game", 120, 250, 160, 50)
        exit_button = draw_button("Exit", 120, 320, 160, 50)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Start game
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Game function
def game_loop():
    bird_y = BIRD_Y
    velocity = 0
    pipes = []
    def create_pipe():
        height = random.randint(100, 400)
        pipes.append([WIDTH, height])
    create_pipe()
    running = True
    clock = pygame.time.Clock()
    score = 0
    high_score = load_high_score()
    
    while running:
        screen.blit(background, (0, 0))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = JUMP_STRENGTH
                    flap_sound.play()
        
        # Bird movement
        velocity += GRAVITY
        bird_y += velocity
        screen.blit(bird_image, (BIRD_X, int(bird_y)))
        
        # Pipe movement & collision detection
        for pipe in pipes:
            pipe[0] -= SPEED
            screen.blit(pipe_image, (pipe[0], pipe[1] - pipe_image.get_height()))
            screen.blit(pipe_image, (pipe[0], pipe[1] + PIPE_GAP))
            
            if (BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + PIPE_WIDTH):
                if bird_y - BIRD_RADIUS < pipe[1] or bird_y + BIRD_RADIUS > pipe[1] + PIPE_GAP:
                    hit_sound.play()
                    running = False
            
            if pipe[0] + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                create_pipe()
                score += 1
                point_sound.play()
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
        
        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(30)
    
    game_over()

def game_over():
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        font = pygame.font.SysFont(None, 40)
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (140, 100))
        retry_button = draw_button("Retry", 120, 250, 160, 50)
        menu_button = draw_button("Main Menu", 120, 320, 160, 50)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return game_loop()
                if menu_button.collidepoint(event.pos):
                    return main_menu()

# Run the game
while True:
    main_menu()
    game_loop()
