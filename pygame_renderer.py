import pygame
from ui import DrawCommand, DrawRect, Color

def ui_color_to_pg_color(color: Color) -> pygame.Color:
    return pygame.Color(color.r, color.g, color.b)

def render_draw_commands(surface: pygame.Surface, draw_commands: list[DrawCommand]) -> None:
    for command in draw_commands:
        if isinstance(command, DrawRect):
            pygame.draw.rect(
                surface=surface,
                color=ui_color_to_pg_color(command.color),
                rect=(command.x, command.y, command.width, command.height),
            )
