from pprint import pprint

import pygame

from ui import UI, Color, render
from pygame_renderer import render_draw_commands

def Box() -> 'UI':
    return UI().sizing_fixed(100, 100).background(Color(0, 255, 0))

def Row() -> 'UI':
    return UI().top_to_bottom().child_gap(20)

def render_ui() -> None:
    with (UI()
            .background(Color(255, 255, 255))
            .sizing_fixed(screen.get_width(), screen.get_height())
            .spacing(20)
          ):
        with (UI()
                .sizing_fit()
                .background(Color(0, 0, 0))
                .spacing(20)
              ):
            with Row():
                Box().close()
                Box().close()
            with Row():
                Box().close()
                Box().close()

# quick thingy for rendering ui (using pygame renderer)

pygame.init()

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

pygame.display.set_caption('PyUI')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 0, 255))

    render_ui()
    draw_commands = render()
    render_draw_commands(screen, draw_commands)

    pygame.display.update()
    clock.tick(60)
