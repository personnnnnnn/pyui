import pygame

from ui import UI, Color, render, Text
from pygame_renderer import Renderer

# ui hierarchy here
def render_ui() -> None:
    with UI().background(Color(255, 255, 255)).sizing_fixed(screen.get_width(), screen.get_height()).spacing(20):
        with UI().background(Color(0, 255, 0)).width_grow().height_fit().spacing(10):
            Text('One two three').font_size(15).show()
            UI().width_grow().show()
            Text('Four five six').font_size(15).show()

pygame.init()

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

pygame.display.set_caption('PyUI')

renderer = Renderer(font_path='arial.ttf')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 0, 255))

    # render the ui here
    render_ui()
    draw_commands = render()
    renderer.render_draw_commands(screen, draw_commands)

    pygame.display.update()
    clock.tick(60)
