import pygame
from dataclasses import dataclass
from .colors import BLACK, YELLOW, GRAY, OLIVE, GREEN, RED


@dataclass
class Cap:
    letter: str
    bg_color: str
    number: int
    pos: tuple
    guessed: bool = False
    selected: bool = False

    @property
    def rect(self):
        return pygame.Rect(self.pos[0] - 10, self.pos[1] - 10, 50, 90)

    def select_cap(self):
        self.selected = True
        self.bg_color = YELLOW

    def deselect_cap(self):
        self.selected = False
        self.bg_color = GRAY

    def is_clicked(self, mouse_pos):
        """checks wheter the cap has been clicked or not"""
        if self.guessed:
            return False
        x, y = self.pos
        cap_width, cap_height = 50, 90

        if self.number and (
            x - 10 < mouse_pos[0] < x + cap_width - 10
            and y - 10 < mouse_pos[1] < y + cap_height - 10
        ):
            self.select_cap()
            return True
        self.deselect_cap()
        return False

    def draw(self, font, screen):
        if self.number:
            # Draw the cap with centered background and numbers
            pygame.draw.rect(screen, self.bg_color, self.rect, 0)

            # Display the correct letter if guessed correctly
            if self.guessed:
                letter_surface = font.render(self.letter, True, BLACK)
                screen.blit(
                    letter_surface, (self.pos[0] + 10, self.pos[1])
                )  # Center the letter inside the cap
                number_surface = font.render(str(self.number), True, BLACK)
                screen.blit(number_surface, (self.pos[0] + 8, self.pos[1] + 40))

            else:
                letter_surface = font.render("_", True, BLACK)
                screen.blit(letter_surface, (self.pos[0] + 10, self.pos[1]))

                number_surface = font.render(str(self.number), True, BLACK)
                screen.blit(
                    number_surface,
                    (
                        self.pos[0] + 9,
                        self.pos[1] + 40,
                    ),
                )
