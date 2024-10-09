import pygame
from game.colors import WHITE, BG_COLOR, GREEN, RED
from game.utils import (
    map_number_to_letters,
    generate_keyboard,
    arrange_caps,
    get_new_phrase,
)

pygame.init()
clock = pygame.time.Clock()
fps = 60

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Phrase Guessing Game")


# Game variables
phrase = get_new_phrase()
lives = 10
guessed_letters = set()  # Store guessed letters
selected_cap = None  # Currently selected cap
selected_key = None  # Currently selected key


# Set fonts
font = pygame.font.Font(None, 55)
cap_font = pygame.font.Font(None, 24)
key_font = pygame.font.Font(None, 34)


# Extra


def check_guess(key, cap):
    """Check if the guessed letter is correct for the selected cap."""
    global lives, selected_cap, selected_key
    if selected_cap is None or key.letter in guessed_letters:
        return  # No cap selected or letter already guessed, do nothing

    correct_letter = cap.letter
    key_letter = key.letter

    # Compare the guessed letter with the correct letter for the selected cap
    if key_letter == correct_letter:
        guessed_letters.add(key.letter)  # Add the correct letter to guessed letters

        filtered_caps = list(filter(lambda c: c.letter == key_letter, caps))
        for cap in filtered_caps:
            cap.guessed = True
            cap.bg_color = GREEN

            # Disable the key
            key.disable = True
            key.bg_color = WHITE
            key.text_color = WHITE
            selected_key = None

    else:
        cap.bg_color = GREEN
        key.bg_color = RED
        lives -= 1  # Wrong guess, lose a life

    selected_cap = None  # Deselect the cap after guessing


caps, letter_to_number = map_number_to_letters(phrase)


keys = generate_keyboard()

arrange_caps(caps, screen_width)
# End of Extra


# Game loop
running = True
clicked = False

while running:
    clock.tick(fps)
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()
    mouse_over_cap = False
    mouse_over_key = False

    # keys loop
    for key in keys:
        key.draw(key_font, screen)
        if key.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            mouse_over_key = True
            if clicked and selected_cap:
                click_singal = key.is_clicked(mouse_pos)
                if click_singal:
                    if selected_key and selected_key != key:
                        selected_key.deselect()
                    selected_key = key
                    check_guess(selected_key, selected_cap)
    # caps loop
    for cap in caps:
        if clicked:
            clicked_cap_signal = cap.is_clicked(mouse_pos)
            if clicked_cap_signal:
                selected_cap = cap
        cap.draw(cap_font, screen)
        if cap.rect.collidepoint(mouse_pos) and cap.number:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            mouse_over_cap = True

    if not mouse_over_cap and not mouse_over_key:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        else:
            clicked = False

    pygame.display.update()


pygame.quit()
