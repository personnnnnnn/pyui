import pygame
from ui import DrawCommand, DrawRect, DrawText, Color, UIFont, UI

def ui_color_to_pg_color(color: Color) -> pygame.Color:
    return pygame.Color(color.r, color.g, color.b)


class PygameFont(UIFont):
    def __init__(self, font_path: str) -> None:
        super().__init__()
        self.font_path = font_path

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
    def __init__(self):
        UI.set_text_measurer(self.text_measurer)

    def load_font(self, font_path: str) -> PygameFont:
        return PygameFont(font_path)

    def render_draw_commands(self, surface: pygame.Surface, draw_commands: list[DrawCommand]) -> None:
        for command in draw_commands:
            if isinstance(command, DrawRect):
                pygame.draw.rect(
                    surface=surface,
                    color=ui_color_to_pg_color(command.color),
                    rect=(command.x, command.y, command.width, command.height),
                )
            elif isinstance(command, DrawText):
                if not isinstance(command.font, PygameFont):
                    raise Exception('Cannot use non-pygame font in pygame renderer!')
                text_surf = command.font.get_font(command.font_size).render(command.text, True, ui_color_to_pg_color(command.color))
                surface.blit(text_surf, (command.x, command.y))
