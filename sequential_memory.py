import pygame
import random
import os
import sys
import time

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sequential Memory Game")
FPS = 60
FONT = pygame.font.Font('assets/PlaywriteHU-VariableFont_wght.ttf', 24)  # Smaller font for End Game button

# --- Music ---
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('assets', 'mrt_jingle.mp3'))
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

# --- Load Icons ---
ASSET_FOLDER = 'assets'
ICON_NAMES = [
    "chilli_crab.png", "marina_bay_sands.png", "changi_airport.png",
    "art_sci_museum.png", "singapore_flyer.jpg", "merlion.png", "GBTB.jpg"
]

def load_icon(name):
    path = os.path.join(ASSET_FOLDER, name)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, (120, 120))

ICONS = {name: load_icon(name) for name in ICON_NAMES}

# --- GameIcon class ---
class GameIcon:
    def __init__(self, name, pos):
        self.name = name
        self.image = ICONS[name]
        self.rect = self.image.get_rect(topleft=pos)
        self.clicked = False
        self.hovered = False

    def draw(self, screen):
        # Light border if hovered
        if self.hovered:
            pygame.draw.rect(screen, (153, 175, 215), self.rect.inflate(6, 6), border_radius=12)
        # Green border if clicked
        if self.clicked:
            pygame.draw.rect(screen, (68, 112, 173), self.rect.inflate(8, 8), 4, border_radius=12)
        screen.blit(self.image, self.rect.topleft)

# --- Draw text centered ---
def draw_text_center(text, y_offset=50):
    rendered = FONT.render(text, True, (0, 0, 0))
    SCREEN.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, y_offset))

# --- Show sequence one-by-one ---
def display_sequence(sequence):
    SCREEN.fill((255, 255, 255))
    draw_text_center("Memorize the sequence")
    pygame.display.flip()
    time.sleep(1.5)

    for icon in sequence:
        SCREEN.fill((255, 255, 255))
        icon.draw(SCREEN)
        pygame.display.flip()
        time.sleep(1.2)
        SCREEN.fill((255, 255, 255))
        pygame.display.flip()
        time.sleep(0.5)

# --- Draw End Game Button ---
def draw_end_button():
    button_width = 80
    button_height = 50
    end_button = pygame.Rect(WIDTH - button_width - 20, HEIGHT - button_height - 20, button_width, button_height)
    pygame.draw.rect(SCREEN, (220, 60, 60), end_button, border_radius=6)
    text = FONT.render("End", True, (255, 255, 255))
    SCREEN.blit(text, (end_button.x + (button_width - text.get_width()) // 2, end_button.y + 5))
    return end_button

# --- Main Game Loop ---
def main():
    clock = pygame.time.Clock()
    game_state = "start"
    sequence = []
    options = []
    user_sequence = []
    correct_order = []
    end_button = None

    while True:
        clock.tick(FPS)
        SCREEN.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        # --- Game State Handling ---
        if game_state == "start":
            draw_text_center("Click anywhere to start the memory game")

        elif game_state == "show_sequence":
            chosen_targets = random.sample(ICON_NAMES, 3)
            print()
            print("----------------- GAME START -----------------")
            print('chosen_targets', chosen_targets)
            distractors = random.sample([i for i in ICON_NAMES if i not in chosen_targets], 2)
            correct_order = chosen_targets[:]
            sequence = [GameIcon(name, ((WIDTH - 120) // 2, (HEIGHT - 120) // 2)) for name in correct_order]
            display_sequence(sequence) # to display the correct sequence to the user

            all_icons = correct_order + distractors
            random.shuffle(all_icons)
            spacing = WIDTH // (len(all_icons) + 1)
            options = []
            for i, name in enumerate(all_icons):
                pos = (spacing * (i + 1) - 60, HEIGHT // 2 + 80)
                options.append(GameIcon(name, pos))

            print('options', [opt.name for opt in options])

            user_sequence = []
            game_state = "recall"

        elif game_state == "recall":
            draw_text_center("Click the icons in the order you saw them.")
            for icon in options:
                icon.hovered = icon.rect.collidepoint(mouse_pos)
                icon.draw(SCREEN)
            end_button = draw_end_button()
            

        elif game_state == "result":
            print('user_sequence result', user_sequence)
            print('correct_order', correct_order)
            is_correct = user_sequence == correct_order
            draw_text_center("Correct!" if is_correct else "Oops! Try again.")

            pygame.display.flip()
            time.sleep(2)
            game_state = "start"

        pygame.display.flip()

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    game_state = "show_sequence"

                elif game_state == "recall":
                    for icon in options:
                        if icon.rect.collidepoint(event.pos):
                            if icon.clicked:
                                icon.clicked = False
                                if icon.name in user_sequence:
                                    user_sequence.remove(icon.name)
                            else:
                                icon.clicked = True
                                user_sequence.append(icon.name)
                            break  # stop after the first match


                    if end_button and end_button.collidepoint(event.pos):
                        game_state = "result"

if __name__ == "__main__":
    main()
