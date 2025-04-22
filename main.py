import pygame

from ui import UI, Color, render, Text
from pygame_renderer import Renderer

def StyledText(text: str) -> None:
    Text(text).font_size(20).color(Color(100, 100, 100)).show()

def Title(text: str) -> None:
    Text(text).font_size(40).color(Color(100, 100, 100)).show()


def Section() -> UI:
    return UI().background(Color(220, 220, 220)).spacing(10)

# ui hierarchy here
def render_ui() -> None:
    with UI().background(Color(255, 255, 255)).sizing_fixed(screen.get_width(), screen.get_height()).padding(20).child_gap(10).top_to_bottom():
        with Section().width_grow():
            StyledText('Home')
            UI().width_grow().show()
            StyledText('File')
            StyledText('Exit')
        with UI().sizing_grow().child_gap(10):
            with Section().height_grow().top_to_bottom():
                StyledText('Document 1')
                StyledText('Document 2')
            with Section().sizing_grow().top_to_bottom().padding(10):
                Title('Title')
                StyledText('Content')

pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
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
