from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int


class DrawCommand:
    ...


@dataclass
class DrawRect(DrawCommand):
    x: float
    y: float
    width: float
    height: float
    color: Color


class Sizing: ...


class Fit(Sizing): ...


@dataclass
class Fixed(Sizing): pixels: float


class LayoutDirection: ...


class LeftToRight(LayoutDirection): ...


class TopToBottom(LayoutDirection): ...


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
    layout_direction: LayoutDirection = LeftToRight()


@dataclass
class ElementData:
    width: float = 0
    height: float = 0


class UI:
    current_element: list['UI'] = []
    root_element: 'UI' = None

    def get_ui_length_across(self, x_axis: bool) -> Sizing:
        return self.ui_data.width if x_axis else self.ui_data.height

    def get_ui_length_perpen(self, x_axis: bool) -> Sizing:
        return self.get_ui_length_across(not x_axis)

    def get_length_across(self, x_axis: bool) -> float:
        return self.element_data.width if x_axis else self.element_data.height

    def get_length_perpen(self, x_axis: bool) -> float:
        return self.get_length_across(not x_axis)

    def set_length_across(self, x_axis: bool, length: float) -> None:
        if x_axis:
            self.element_data.width = length
        else:
            self.element_data.height = length

    def set_length_perpen(self, x_axis: bool, length: float) -> float:
        self.set_length_across(not x_axis, length)

    def get_padding_across(self, x_axis: bool) -> float:
        return self.ui_data.padding_left + self.ui_data.padding_right if x_axis else self.ui_data.padding_top + self.ui_data.padding_bottom

    def get_padding_perpen(self, x_axis: bool) -> float:
        return self.get_padding_across(not x_axis)

    def x_axis(self) -> bool:
        return isinstance(self.ui_data.layout_direction, LeftToRight)

    def __init__(self):
        self.ui_data = UIData()
        self.element_data = ElementData()
        self.children: list['UI'] = []
        self.parent: 'UI' = None

    def __enter__(self) -> 'UI':
        return self.__open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__exit()

    def __open(self) -> 'UI':
        if len(UI.current_element) != 0:
            UI.current_element[-1].children.append(self)
            self.parent = UI.current_element[-1]
        else:
            UI.root_element = self
        UI.current_element.append(self)
        return self

    def __add_padding_to_dimensions_axis(self, x_axis: bool) -> None:
        if isinstance(self.get_ui_length_across(x_axis), Fixed):
            return
        self.set_length_across(x_axis, self.get_length_across(x_axis) + self.get_padding_across(x_axis))
        if x_axis == self.x_axis():
            child_gap = max(0, len(self.children) - 1) * self.ui_data.child_gap
            self.set_length_across(x_axis, self.get_length_across(x_axis) + child_gap)

    def __add_padding_to_dimensions(self) -> None:
        self.__add_padding_to_dimensions_axis(True)
        self.__add_padding_to_dimensions_axis(False)

    def __add_dimensions_to_parent(self) -> None:
        if self.parent is None:
            return
        x_axis = self.parent.x_axis()
        if not isinstance(self.parent.get_ui_length_across(x_axis), Fixed):
            self.parent.set_length_across(x_axis,
                                          self.parent.get_length_across(x_axis) + self.get_length_across(x_axis))
        if not isinstance(self.parent.get_ui_length_perpen(x_axis), Fixed):
            self.parent.set_length_perpen(x_axis,
                                          max(self.parent.get_padding_perpen(x_axis), self.get_length_perpen(x_axis)))

    def __exit(self) -> 'UI':
        UI.current_element.pop()

        if isinstance(self.ui_data.width, Fixed):
            self.element_data.width += self.ui_data.width.pixels
        if isinstance(self.ui_data.height, Fixed):
            self.element_data.height += self.ui_data.height.pixels

        self.__add_padding_to_dimensions()
        self.__add_dimensions_to_parent()

        return self

    def close(self) -> 'UI':
        return self.__open().__exit()

    def background(self, color: Color | None) -> 'UI':
        self.ui_data.background_color = color
        return self

    def no_background(self) -> 'UI':
        return self.background(None)

    def padding_left(self, padding: float) -> 'UI':
        self.ui_data.padding_left = padding
        return self

    def padding_right(self, padding: float) -> 'UI':
        self.ui_data.padding_right = padding
        return self

    def padding_top(self, padding: float) -> 'UI':
        self.ui_data.padding_top = padding
        return self

    def padding_bottom(self, padding: float) -> 'UI':
        self.ui_data.padding_bottom = padding
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
        self.ui_data.child_gap = gap
        return self

    def no_child_gap(self) -> 'UI':
        return self.child_gap(0)

    def spacing(self, spacing: float) -> 'UI':
        return self.child_gap(spacing).padding(spacing)

    def no_spacing(self) -> 'UI':
        return self.spacing(0)

    def width(self, sizing: Sizing) -> 'UI':
        self.ui_data.width = sizing
        return self

    def height(self, sizing: Sizing) -> 'UI':
        self.ui_data.height = sizing
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

    def layout_direction(self, direction: LayoutDirection) -> 'UI':
        self.ui_data.layout_direction = direction
        return self

    def top_to_bottom(self) -> 'UI':
        return self.layout_direction(TopToBottom())

    def left_to_right(self) -> 'UI':
        return self.layout_direction(LeftToRight())

    def render(self, draw_commands: list['DrawCommand'] | None = None, x: float = 0, y: float = 0) -> list['DrawCommand']:
        if draw_commands is None:
            draw_commands = []

        if self.ui_data.background_color is not None:
            draw_commands.append(DrawRect(
                x=x,
                y=y,
                width=self.element_data.width,
                height=self.element_data.height,
                color=self.ui_data.background_color,
            ))

        x += self.ui_data.padding_left
        y += self.ui_data.padding_top

        x_axis = self.x_axis()

        for child in self.children:
            child.render(draw_commands, x, y)
            increment = self.ui_data.child_gap + child.get_length_across(x_axis)
            if x_axis:
                x += increment
            else:
                y += increment

        return draw_commands


def render(x: float = 0, y: float = 0) -> list['DrawCommand']:
    return UI.root_element.render(x=x, y=y)
