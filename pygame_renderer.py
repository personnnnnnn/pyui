import pygame
from ui import DrawCommand, DrawRect, DrawText, Color, TextMeasurer, UI

def ui_color_to_pg_color(color: Color) -> pygame.Color:
    return pygame.Color(color.r, color.g, color.b)


class PygameTextMeasurer(TextMeasurer):
    def __init__(self, font_path: str) -> None:
        self.font_path = font_path  # Save path to font file

    def get_font(self, font_size: float) -> pygame.font.Font:
        return pygame.font.Font(self.font_path, int(font_size))

    def get_text_height(self, font_size: float) -> float:
        font = self.get_font(font_size)
        return font.get_height()

    def get_text_width(self, text: str, font_size: float) -> float:
        font = self.get_font(font_size)
        width, _ = font.size(text)
        return width

class Renderer:
    def __init__(self, font_path: str):
        self.font_path = font_path
        self.text_measurer = PygameTextMeasurer(self.font_path)
        UI.set_text_measurer(self.text_measurer)

    def render_draw_commands(self, surface: pygame.Surface, draw_commands: list[DrawCommand]) -> None:
        for command in draw_commands:
            if isinstance(command, DrawRect):
                pygame.draw.rect(
                    surface=surface,
                    color=ui_color_to_pg_color(command.color),
                    rect=(command.x, command.y, command.width, command.height),
                )
            elif isinstance(command, DrawText):
                text_surf = self.text_measurer.get_font(command.font_size).render(command.text, True, ui_color_to_pg_color(command.color))
                # for debugging
                # pygame.draw.rect(
                #     surface=surface,
                #     color=ui_color_to_pg_color(Color(255, 0, 0)),
                #     rect=(command.x, command.y, UI.text_measurer.get_text_width(command.text, command.font_size),
                #           UI.text_measurer.get_text_height(command.font_size)),
                # )
                surface.blit(text_surf, (command.x, command.y))
