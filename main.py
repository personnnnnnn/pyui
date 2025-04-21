from ui import UI, Color

def render_ui() -> None:
    with (UI()
            .background(Color(255, 255, 255))
            .sizing_fixed(400, 400)
            .spacing(20)):
        UI().sizing_fit().background(Color(0, 0, 0)).close()


