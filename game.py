import pygame
import random

pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Phrase Guessing Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)
BG_COLOR = (240, 240, 240)

# Set fonts
font = pygame.font.Font(None, 55)
small_font = pygame.font.Font(None, 34)

# Game variables
phrase = "YOU CAN DO IT"
caps = []  # List of caps (numbers) associated with phrase letters
lives = 10
guessed_letters = set()  # Store guessed letters
selected_cap = None  # Currently selected cap
cap_colors = []  # Color for each cap
cap_letters = []  # Store the correct letters for each cap
letter_to_number = {}  # Dictionary to store the number for each letter



# Assign a unique number for each letter in the phrase
for letter in phrase:
    if letter != " ":
        if letter not in letter_to_number:
            number = random.randint(1, 26)
            letter_to_number[
                letter
            ] = number  # Assign the same number to all occurrences of the letter

        caps.append(letter_to_number[letter])
        cap_colors.append(GRAY)  # Default color for caps
        cap_letters.append(letter)
    else:
        caps.append(" ")
        cap_colors.append(WHITE)  # Space color
        cap_letters.append(" ")

# Keyboard layout
keyboard_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


def draw_phrase():
    """Draws the current state of the phrase with caps and numbers."""
    x, y = 50, 150
    for idx, number in enumerate(caps):
        if number == " ":
            x += 50  # Space between words
            continue

        # Check if this cap is selected
        cap_color = cap_colors[idx]
        if selected_cap == idx:
            cap_color = YELLOW  # Highlight selected cap

        # Draw the cap with centered background color and numbers
        pygame.draw.rect(
            screen, cap_color, (x - 10, y - 10, 50, 90), 0
        )  # Cap background

        # Display the correct letter if guessed correctly

        if cap_letters[idx] in guessed_letters:
            letter_surface = font.render(cap_letters[idx], True, BLACK)
            screen.blit(letter_surface, (x + 8, y))  # Center the letter inside the cap
        else:
            letter_surface = font.render("_", True, BLACK)
            screen.blit(letter_surface, (x + 8, y))

        # Display the number exactly under the cap, centered
        number_surface = small_font.render(str(number), True, BLACK)
        screen.blit(number_surface, (x + 10, y + 60))  # Center the number under the cap
        x += 50  # Space between letters


def draw_keyboard():
    """Draw the on-screen keyboard for letter selection."""
    x_start, y_start = 50, 400
    key_width, key_height = 50, 50
    gap = 10

    for row in keyboard_layout:
        x = x_start
        for letter in row:
            color = WHITE if letter not in guessed_letters else DARK_GRAY
            pygame.draw.rect(
                screen, color, (x, y_start, key_width, key_height), border_radius=8
            )
            letter_surface = small_font.render(letter, True, BLACK)
            screen.blit(letter_surface, (x + 15, y_start + 10))
            x += key_width + gap
        y_start += key_height + gap


def get_clicked_letter(mouse_pos):
    """Returns the letter clicked on the keyboard, or None if none clicked."""
    x_start, y_start = 50, 400
    key_width, key_height = 50, 50
    gap = 10

    for row in keyboard_layout:
        x = x_start
        for letter in row:
            if (
                x < mouse_pos[0] < x + key_width
                and y_start < mouse_pos[1] < y_start + key_height
            ):
                return letter
            x += key_width + gap
        y_start += key_height + gap
    return None


def get_clicked_cap(mouse_pos):
    """Returns the index of the clicked cap, or None if none clicked."""
    x, y = 50, 150
    cap_width, cap_height = 50, 90

    for idx, number in enumerate(caps):
        if number == " ":
            x += 50
            continue

        if (
            x - 10 < mouse_pos[0] < x + cap_width - 10
            and y - 10 < mouse_pos[1] < y + cap_height - 10
        ):
            return idx
        x += 50
    return None


def check_guess(letter):
    """Check if the guessed letter is correct for the selected cap."""
    global lives, selected_cap
    if selected_cap is None or letter in guessed_letters:
        return  # No cap selected or letter already guessed, do nothing

    correct_letter = cap_letters[selected_cap]

    # Compare the guessed letter with the correct letter for the selected cap
    if letter == correct_letter:
        guessed_letters.add(letter)  # Add the correct letter to guessed letters
        for idx, cap_letter in enumerate(cap_letters):
            if cap_letter == letter:
                cap_colors[
                    idx
                ] = GREEN  # Turn all identical caps green for correct guess
    else:
        cap_colors[selected_cap] = RED  # Turn cap red for wrong guess
        lives -= 1  # Wrong guess, lose a life

    selected_cap = None  # Deselect the cap after guessing


# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_phrase()
    draw_keyboard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if lives == 0:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if a cap was clicked
            clicked_cap = get_clicked_cap(mouse_pos)
            if clicked_cap is not None:
                selected_cap = clicked_cap  # Select the cap

            # Check if a keyboard letter was clicked
            clicked_letter = get_clicked_letter(mouse_pos)
            if clicked_letter and selected_cap is not None:
                check_guess(clicked_letter)

    pygame.display.update()

pygame.quit()
