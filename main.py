from ui import UI, Color, render


def render_ui() -> None:
    with (UI()
            .background(Color(255, 255, 255))
            .sizing_fixed(400, 400)
            .spacing(20)
          ) as root:
        with (UI()
                .sizing_fit()
                .background(Color(0, 0, 0))
                .spacing(20)
              ):
            UI().sizing_fixed(200, 200).close()
    print(root)

render_ui()
render()
