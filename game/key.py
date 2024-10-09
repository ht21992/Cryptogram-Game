from dataclasses import dataclass
import pygame
from .colors import BLACK, WHITE, DARK_GRAY, YELLOW


@dataclass
class Key:
    letter: str
    pos: tuple
    size: tuple
    bg_color: str = WHITE
    text_color: str = BLACK
    selected: bool = False
    disable: bool = False

    @property
    def rect(self):
        key_width, key_height = self.size[0], self.size[1]
        x, y = self.pos[0], self.pos[1]
        return pygame.Rect(x, y, key_width, key_height)

    def deselect(self):
        self.selected = False
        self.bg_color = WHITE
        self.text_color = BLACK

    def is_clicked(self, mouse_pos):
        """checks wheter the key has been clicked or not"""
        if self.disable:
            self.bg_color = WHITE
            self.text_color = WHITE
            return False

        x, y = self.pos
        key_width, key_height = self.size

        if (
            x < mouse_pos[0] < x + key_width
            and y < mouse_pos[1] < y + key_height
            and not self.selected
        ):
            self.selected = True
            self.bg_color = YELLOW
            return True

        return False

    def draw(self, font, screen):
        key_width, key_height = self.size[0], self.size[1]
        x, y = self.pos[0], self.pos[1]
        pygame.draw.rect(
            screen, self.bg_color, (x, y, key_width, key_height), border_radius=8
        )
        letter_surface = font.render(self.letter, True, self.text_color)
        screen.blit(letter_surface, (x + 15, y + 10))
