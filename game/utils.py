import random
from game.cap import Cap
from .colors import GRAY, WHITE, DARK_GRAY
from .key import Key


def get_new_phrase() -> str:
    phrases = [
        "You Can Do It",
        "Never Give Up",
        "Stay Strong",
        "Keep Going",
        "Success",
        "Dream Big",
        "One Step At A Time",
        "You Got it",
        "Be Bold",
        "Be Focused",
        "Succession",
        "House",
        "On A Fleek",
    ]

    return random.choice(phrases).upper()


def map_number_to_letters(phrase):
    if len(phrase) > 19:
        phrase = "YOU CAN DO IT"
    x, y = 50, 150
    caps = []
    letter_to_number = {}
    numbers = list(range(1, 26))
    for letter in phrase:
        if letter.strip():
            if letter not in letter_to_number:
                number = random.choice(numbers)
                letter_to_number[
                    letter
                ] = number  # Assign the same number to all occurrences of the letter
                numbers.remove(number)
            cap = Cap(letter, GRAY, letter_to_number[letter], (x, y))
            caps.append(cap)

        else:
            cap = Cap("", WHITE, 0, (x, y))
            caps.append(cap)

        x += 50

    return caps, letter_to_number


def generate_keyboard() -> list:
    """Prepare keyboard keys and returns a list of keys"""
    keys = []
    x_start, y_start = 40, 400
    key_width, key_height = 50, 50
    gap = 7
    keyboard_layout = ["QWERTYUIOASBN", "DFGHJKLZXCVMP"]
    for row in keyboard_layout:
        x = x_start
        for letter in row:
            # color = WHITE
            # color = WHITE if letter not in guessed_letters else DARK_GRAY
            pos = (x, y_start)
            size = (key_width, key_height)
            key = Key(letter, pos, size)
            keys.append(key)

            x += key_width + gap
        y_start += key_height + gap

    return keys


def arrange_caps(caps, screen_width, cap_width=60, cap_spacing=10, row_spacing=100):
    """
    Arrange caps into multiple rows to fit within the screen width.

    Args:
        caps (list): The list of Cap objects.
        screen_width (int): The width of the screen.
        cap_width (int): The width of a cap.
        cap_spacing (int): The spacing between caps.
        row_spacing (int): The vertical spacing between rows.
    """
    max_caps_per_row = screen_width // (cap_width + cap_spacing)
    current_x, current_y = 50, 150  # Initial position for first row
    current_row_count = 0

    for i, cap in enumerate(caps):
        cap.pos = (current_x, current_y)

        # Move to the next cap position
        current_x += cap_width + cap_spacing
        current_row_count += 1

        # If the row is full, move to the next row
        if current_row_count >= max_caps_per_row:
            current_x = 50  # Reset X for new row
            current_y += row_spacing  # Move down to the next row
            current_row_count = 0  # Reset row count for the new row
