from dataclasses import dataclass

@dataclass
class Color:
    r: int
    g: int
    b: int

class Sizing:
    ...

class Fit(Sizing):
    ...

@dataclass
class Fixed(Sizing):
    pixels: float

@dataclass
class UIData:
    background_color: Color | None = None
    padding_left: float = 0
    padding_right: float = 0
    padding_top: float = 0
    padding_bottom: float = 0
    child_gap: float = 0
    width: Sizing = Fit()
    height: Sizing = Fit()

class UI:
    __current_element: list['UI'] = []

    def __init__(self):
        self.data = UIData()
        self.children: list['UI'] = []
        self.parent: 'UI' = None

    def __enter__(self):
        if len(UI.__current_element) == 0:
            UI.__current_element[-1].children.append(self)
            self.parent = UI.__current_element[-1]
        UI.__current_element.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        UI.__current_element.pop()

    def background(self, color: Color | None) -> 'UI':
        self.data.background_color = color
        return self

    def no_background(self) -> 'UI':
        return self.background(None)

    def padding_left(self, padding: float) -> 'UI':
        self.data.padding_left = padding
        return self

    def padding_right(self, padding: float) -> 'UI':
        self.data.padding_right = padding
        return self

    def padding_top(self, padding: float) -> 'UI':
        self.data.padding_top = padding
        return self

    def padding_bottom(self, padding: float) -> 'UI':
        self.data.padding_bottom = padding
        return self

    def padding_hor(self, padding: float) -> 'UI':
        return self.padding_left(padding).padding_right(padding)

    def padding_ver(self, padding: float) -> 'UI':
        return self.padding_top(padding).padding_bottom(padding)

    def padding(self, padding: float) -> 'UI':
        return self.padding_ver(padding).padding_hor(padding)

    def no_padding(self) -> 'UI':
        return self.padding(0)

    def child_gap(self, gap: float) -> 'UI':
        self.data.child_gap = gap
        return self

    def no_child_gap(self) -> 'UI':
        return self.child_gap(0)

    def spacing(self, spacing: float) -> 'UI':
        return self.child_gap(spacing).padding(spacing)

    def no_spacing(self) -> 'UI':
        return self.spacing(0)

    def width(self, sizing: Sizing) -> 'UI':
        self.data.width = sizing
        return self

    def height(self, sizing: Sizing) -> 'UI':
        self.data.height = sizing
        return self

    def width_fit(self) -> 'UI':
        return self.width(Fit())

    def height_fit(self) -> 'UI':
        return self.height(Fit())

    def sizing_fit(self) -> 'UI':
        return self.width_fit().height_fit()

    def width_fixed(self, width: float) -> 'UI':
        return self.width(Fixed(width))

    def height_fixed(self, height: float) -> 'UI':
        return self.height(Fixed(height))

    def sizing_fixed(self, width: float, height: float) -> 'UI':
        return self.width_fixed(width).height_fixed(height)







