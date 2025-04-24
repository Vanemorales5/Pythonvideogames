import pygame
import random
import math
import os
from pygame import mixer

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hamster Heroes")

# Game states
SPLASH = 0
MENU = 1
GAME = 2
INSTRUCTIONS = 3
GAME_OVER = 4
WIN = 5

current_state = SPLASH
score_value = 0
high_score = 0
level = 1
start_time = 0
splash_start_time = 0
game_over_reason = ""

# Load images - using your specific filenames
print("Loading images...")
try:
    # Try to load background.eps first
    background_img = pygame.image.load('background.eps')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    print("Loaded background.eps")
except:
    # If EPS loading fails, try common formats
    try:
        background_img = pygame.image.load('background.jpg')
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        print("Loaded background.jpg")
    except:
        try:
            background_img = pygame.image.load('background.png')
            background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
            print("Loaded background.png")
        except:
            # Create a simple gradient background if no image is available
            print("No background image found, creating gradient")
            background_img = pygame.Surface((WIDTH, HEIGHT))
            for y in range(HEIGHT):
                # Create a blue to cyan gradient
                color = (100, 150, 255 - y // 3)
                pygame.draw.line(background_img, color, (0, y), (WIDTH, y))

# Load all other game images
print("Loading game images...")
try:
    hamster_img = pygame.image.load('hamster.png')
    hamster_img = pygame.transform.scale(hamster_img, (64, 64))
    print("Loaded hamster.png")

    seed_img = pygame.image.load('seed.png')
    seed_img = pygame.transform.scale(seed_img, (40, 40))
    print("Loaded seed.png")

    carrot_img = pygame.image.load('carrot.png')
    carrot_img = pygame.transform.scale(carrot_img, (16, 32))
    print("Loaded carrot.png")

    sunflower_img = pygame.image.load('sunflower.png')
    sunflower_img = pygame.transform.scale(sunflower_img, (80, 80))
    print("Loaded sunflower.png")
except Exception as e:
    print(f"Error loading game images: {e}")
    print("The game requires hamster.png, seed.png, carrot.png, and sunflower.png")
    print("Please make sure these files are in the same directory as the game script")
    pygame.quit()
    exit()

# Try to load splash screen image
try:
    splash_img = pygame.image.load('splash.png')
    splash_img = pygame.transform.scale(splash_img, (WIDTH, HEIGHT))
    print("Loaded splash.png")
except:
    # Use background as splash if splash.png not available
    print("No splash.png found, using background instead")
    splash_img = background_img.copy()

# Try to load animation frames
hamster_animation = []
try:
    for i in range(1, 5):  # Assuming you have 4 animation frames
        frame = pygame.image.load(f'hamster_frame{i}.png')
        frame = pygame.transform.scale(frame, (64, 64))
        hamster_animation.append(frame)
    print(f"Loaded {len(hamster_animation)} hamster animation frames")
except:
    # If no animation frames, use the static hamster image
    hamster_animation = [hamster_img]
    print("No animation frames found, using static hamster image")

# Load sounds
print("Loading sounds...")
try:
    mixer.music.load('background_music.wav')
    collect_sound = mixer.Sound('collect.wav')
    hit_sound = mixer.Sound('hit.wav')
    click_sound = mixer.Sound('click.wav')
    print("Successfully loaded sound files")
except Exception as e:
    print(f"Could not load sound files: {e}")
    collect_sound = None
    hit_sound = None
    click_sound = None

# Create fonts
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 64)
title_font = pygame.font.Font(None, 80)

# Player (hamster) settings
hamster_x = 370
hamster_y = 480
hamster_speed = 5
hamster_x_change = 0
hamster_width = 64
hamster_height = 64

# Seed (enemy) settings
seeds = []
num_seeds = 4
seed_width = 40
seed_height = 40

# Speed reduction factor for falling objects (seeds and sunflowers)
speed_factor = 0.25  # Reducing speed to 25% of original

# Carrot (bullet) settings
carrots = []
max_carrots = 5
carrot_width = 16
carrot_height = 32

# Sunflower (power-up) settings
sunflowers = []
max_sunflowers = 2
sunflower_width = 80
sunflower_height = 80

# Animation variables
animation_frame = 0
animation_timer = 0
animation_speed = 10  # Frames per second


# Button class for menu
class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border

        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            if click_sound:
                click_sound.play()
            return True
        return False


# Initialize menu buttons
start_button = Button(WIDTH // 2 - 100, 250, 200, 50, "Start Game")
instructions_button = Button(WIDTH // 2 - 100, 320, 200, 50, "Instructions")
quit_button = Button(WIDTH // 2 - 100, 390, 200, 50, "Quit Game")
menu_button = Button(WIDTH // 2 - 100, 450, 200, 50, "Main Menu")
play_again_button = Button(WIDTH // 2 - 100, 380, 200, 50, "Play Again")


# Game functions
def reset_game():
    global score_value, level, start_time, seeds, carrots, sunflowers, hamster_x, hamster_y, hamster_x_change

    score_value = 0
    level = 1
    start_time = pygame.time.get_ticks()

    # Reset hamster position
    hamster_x = 370
    hamster_y = 480
    hamster_x_change = 0

    # Initialize seeds
    seeds = []
    for i in range(num_seeds):
        seed = {
            'x': random.randint(0, WIDTH - seed_width),
            'y': random.randint(50, 150),
            'speed_x': random.choice([-3, -2, 2, 3]) * speed_factor,  # Apply speed reduction
            'speed_y': random.randint(1, 3) * level * speed_factor  # Apply speed reduction
        }
        seeds.append(seed)

    # Initialize carrots
    carrots = []
    for i in range(max_carrots):
        carrot = {
            'x': 0,
            'y': 0,
            'speed': 10,
            'state': "ready"  # ready or fired
        }
        carrots.append(carrot)

    # Initialize sunflowers (power-ups)
    sunflowers = []
    for i in range(max_sunflowers):
        sunflower = {
            'x': random.randint(0, WIDTH - sunflower_width),
            'y': -sunflower_height,
            'speed': 2 * speed_factor,  # Apply speed reduction
            'active': False,
            'spawn_time': random.randint(10000, 30000)  # When to spawn in milliseconds
        }
        sunflowers.append(sunflower)


def draw_hamster(x, y):
    # Use animation frames if available
    if len(hamster_animation) > 0:
        frame = hamster_animation[int(animation_frame) % len(hamster_animation)]
        screen.blit(frame, (x, y))
    else:
        # Fallback should never happen as we checked for images
        screen.blit(hamster_img, (x, y))


def draw_seed(x, y):
    screen.blit(seed_img, (x, y))


def draw_carrot(x, y):
    screen.blit(carrot_img, (x, y))


def draw_sunflower(x, y):
    screen.blit(sunflower_img, (x, y))


def fire_carrot(index):
    if carrots[index]['state'] == "ready":
        carrots[index]['x'] = hamster_x + hamster_width // 2 - carrot_width // 2
        carrots[index]['y'] = hamster_y
        carrots[index]['state'] = "fired"
        if collect_sound:
            collect_sound.play()


def is_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    # Simple rectangle collision
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)


def show_text(text, font, color, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)


def draw_splash_screen():
    screen.blit(splash_img, (0, 0))

    # Draw game title
    show_text("HAMSTER HEROES", title_font, (50, 100, 150), WIDTH // 2, 150, True)
    show_text("by Vanessa Morales", font, (50, 50, 50), WIDTH // 2, 220, True)

    # Draw simple hamster animation
    current_time = pygame.time.get_ticks()
    time_passed = current_time - splash_start_time

    # Make the hamster move across the screen
    hamster_pos_x = (time_passed // 10) % WIDTH

    draw_hamster(hamster_pos_x - 64, 350)

    # Show loading text
    dots = "." * ((time_passed // 300) % 4)
    loading_text = f"Loading{dots}"
    show_text(loading_text, font, (0, 0, 0), WIDTH // 2, 500, True)


def draw_menu():
    screen.blit(background_img, (0, 0))

    # Draw title
    show_text("HAMSTER HEROES", title_font, (255, 255, 255), WIDTH // 2, 120, True)

    # Draw buttons
    start_button.draw()
    instructions_button.draw()
    quit_button.draw()

    # Draw highscore
    show_text(f"High Score: {high_score}", font, (255, 255, 255), WIDTH // 2, 500, True)


def draw_instructions():
    screen.blit(background_img, (0, 0))

    # Draw title
    show_text("INSTRUCTIONS", big_font, (255, 255, 255), WIDTH // 2, 80, True)

    # Draw instructions
    instructions = [
        "1. Use LEFT and RIGHT arrow keys to move your hamster",
        "2. Press SPACE to throw carrots at falling seeds",
        "3. Avoid letting seeds reach the bottom of the screen",
        "4. Collect sunflowers for bonus points",
        "5. Survive as long as possible to advance levels",
        "6. The game gets harder with each level, but at a slow pace!"
    ]

    for i, line in enumerate(instructions):
        show_text(line, font, (255, 255, 255), 100, 150 + i * 40)

    # Draw back button
    menu_button.draw()


def draw_game_over():
    # Create a semi-transparent overlay on top of the game screen
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Black with alpha
    screen.blit(overlay, (0, 0))

    # Draw game over text
    show_text("GAME OVER", big_font, (255, 0, 0), WIDTH // 2, 200, True)
    show_text(game_over_reason, font, (255, 255, 255), WIDTH // 2, 280, True)
    show_text(f"Score: {score_value}", font, (255, 255, 255), WIDTH // 2, 330, True)

    # Draw buttons
    play_again_button.draw()
    menu_button.draw()


def draw_win_screen():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 100, 0, 200))  # Green with alpha
    screen.blit(overlay, (0, 0))

    # Draw win text
    show_text("YOU WIN!", big_font, (255, 255, 0), WIDTH // 2, 200, True)
    show_text(f"Final Score: {score_value}", font, (255, 255, 255), WIDTH // 2, 280, True)

    # Draw buttons
    play_again_button.draw()
    menu_button.draw()


def draw_game():
    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw sunflowers (behind other objects)
    for sunflower in sunflowers:
        if sunflower['active']:
            draw_sunflower(sunflower['x'], sunflower['y'])

    # Draw seeds
    for seed in seeds:
        draw_seed(seed['x'], seed['y'])

    # Draw carrots
    for carrot in carrots:
        if carrot['state'] == "fired":
            draw_carrot(carrot['x'], carrot['y'])

    # Draw hamster (on top)
    draw_hamster(hamster_x, hamster_y)

    # Draw UI elements
    # Draw score in a nice box
    pygame.draw.rect(screen, (0, 0, 0, 128), (5, 5, 150, 40), border_radius=5)
    show_text(f"Score: {score_value}", font, (255, 255, 255), 10, 10)

    # Draw level in a nice box
    pygame.draw.rect(screen, (0, 0, 0, 128), (5, 45, 150, 40), border_radius=5)
    show_text(f"Level: {level}", font, (255, 255, 255), 10, 50)

    # Draw time in a nice box
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000  # Convert to seconds
    pygame.draw.rect(screen, (0, 0, 0, 128), (WIDTH - 155, 5, 150, 40), border_radius=5)
    show_text(f"Time: {elapsed_time}s", font, (255, 255, 255), WIDTH - 150, 10)


def update_game():
    global score_value, level, high_score, game_over_reason, current_state, animation_frame, animation_timer

    # Update animation frame
    animation_timer += 1
    if animation_timer >= 60 // animation_speed:
        animation_frame = (animation_frame + 1) % len(hamster_animation)
        animation_timer = 0

    # Update hamster position
    global hamster_x
    hamster_x += hamster_x_change

    # Keep hamster within screen bounds
    if hamster_x < 0:
        hamster_x = 0
    elif hamster_x > WIDTH - hamster_width:
        hamster_x = WIDTH - hamster_width

    # Update seeds
    for seed in seeds:
        # Move seed
        seed['x'] += seed['speed_x']
        seed['y'] += seed['speed_y']

        # Bounce off walls
        if seed['x'] <= 0 or seed['x'] >= WIDTH - seed_width:
            seed['speed_x'] *= -1

        # Check if seed hits bottom (game over)
        if seed['y'] > HEIGHT - seed_height:
            game_over_reason = "Seeds reached your hamster's home!"
            current_state = GAME_OVER
            if score_value > high_score:
                high_score = score_value
            return

        # Check collision with hamster (game over)
        if is_collision(seed['x'], seed['y'], seed_width, seed_height,
                        hamster_x, hamster_y, hamster_width, hamster_height):
            game_over_reason = "Your hamster got hit by a seed!"
            current_state = GAME_OVER
            if hit_sound:
                hit_sound.play()
            if score_value > high_score:
                high_score = score_value
            return

    # Update carrots
    for carrot in carrots:
        if carrot['state'] == "fired":
            carrot['y'] -= carrot['speed']

            # Carrot goes off screen
            if carrot['y'] < 0:
                carrot['state'] = "ready"

            # Check collision with seeds
            for seed in seeds[:]:  # Create a copy to avoid modification during iteration
                if is_collision(carrot['x'], carrot['y'], carrot_width, carrot_height,
                                seed['x'], seed['y'], seed_width, seed_height):
                    if hit_sound:
                        hit_sound.play()
                    carrot['state'] = "ready"
                    score_value += 10

                    # Remove seed and add a new one
                    seeds.remove(seed)
                    new_seed = {
                        'x': random.randint(0, WIDTH - seed_width),
                        'y': random.randint(-100, -50),
                        'speed_x': random.choice([-3, -2, 2, 3]) * speed_factor,  # Apply speed reduction
                        'speed_y': random.randint(1, 3) * level * speed_factor  # Apply speed reduction
                    }
                    seeds.append(new_seed)

    # Update sunflowers
    current_time = pygame.time.get_ticks()
    for sunflower in sunflowers:
        if not sunflower['active'] and current_time - start_time > sunflower['spawn_time']:
            sunflower['active'] = True
            sunflower['x'] = random.randint(0, WIDTH - sunflower_width)
            sunflower['y'] = -sunflower_height

        if sunflower['active']:
            sunflower['y'] += sunflower['speed']

            # Sunflower goes off screen
            if sunflower['y'] > HEIGHT:
                sunflower['active'] = False
                sunflower['spawn_time'] = current_time - start_time + random.randint(10000, 30000)

            # Check collision with hamster
            if is_collision(sunflower['x'], sunflower['y'], sunflower_width, sunflower_height,
                            hamster_x, hamster_y, hamster_width, hamster_height):
                if collect_sound:
                    collect_sound.play()
                sunflower['active'] = False
                sunflower['spawn_time'] = current_time - start_time + random.randint(10000, 30000)
                score_value += 50

    # Level progression - increase level every 30 seconds
    elapsed_time = (current_time - start_time) // 1000
    new_level = elapsed_time // 30 + 1

    if new_level > level:
        level = new_level
        # Increase seed speed with level, but keep it reduced
        for seed in seeds:
            seed['speed_y'] = random.randint(1, 3) * level * speed_factor

    # Win condition - reach 1000 points
    if score_value >= 1000:
        current_state = WIN
        if score_value > high_score:
            high_score = score_value


# Main game loop
clock = pygame.time.Clock()
splash_start_time = pygame.time.get_ticks()
reset_game()

# Start background music
try:
    mixer.music.play(-1)
except:
    pass

running = True
while running:
    # Handle events
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == SPLASH:
            if pygame.time.get_ticks() - splash_start_time > 3000:  # 3 seconds splash screen
                current_state = MENU

        elif current_state == MENU:
            start_button.check_hover(mouse_pos)
            instructions_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)

            if start_button.is_clicked(mouse_pos, event):
                current_state = GAME
                reset_game()

            if instructions_button.is_clicked(mouse_pos, event):
                current_state = INSTRUCTIONS

            if quit_button.is_clicked(mouse_pos, event):
                running = False

        elif current_state == INSTRUCTIONS:
            menu_button.check_hover(mouse_pos)

            if menu_button.is_clicked(mouse_pos, event):
                current_state = MENU

        elif current_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hamster_x_change = -hamster_speed
                if event.key == pygame.K_RIGHT:
                    hamster_x_change = hamster_speed
                if event.key == pygame.K_SPACE:
                    # Find the first ready carrot
                    for i, carrot in enumerate(carrots):
                        if carrot['state'] == "ready":
                            fire_carrot(i)
                            break
                if event.key == pygame.K_ESCAPE:
                    current_state = MENU

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and hamster_x_change < 0:
                    hamster_x_change = 0
                if event.key == pygame.K_RIGHT and hamster_x_change > 0:
                    hamster_x_change = 0

        elif current_state == GAME_OVER or current_state == WIN:
            play_again_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)

            if play_again_button.is_clicked(mouse_pos, event):
                current_state = GAME
                reset_game()

            if menu_button.is_clicked(mouse_pos, event):
                current_state = MENU

    # Update game state
    if current_state == GAME:
        update_game()

    # Draw current state
    if current_state == SPLASH:
        draw_splash_screen()
    elif current_state == MENU:
        draw_menu()
    elif current_state == INSTRUCTIONS:
        draw_instructions()
    elif current_state == GAME:
        draw_game()
    elif current_state == GAME_OVER:
        draw_game_over()
    elif current_state == WIN:
        draw_win_screen()

    # Update display
    pygame.display.update()
    clock.tick(60)

pygame.quit()