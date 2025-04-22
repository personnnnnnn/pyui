from dataclasses import dataclass
from abc import ABC

class TextMeasurer(ABC):
    def get_text_height(self, font_size: float) -> float:
        ...

    def get_text_width(self, text: str, font_size: float) -> float:
        ...

@dataclass
class Color:
    r: int
    g: int
    b: int


class DrawCommand: ...


@dataclass
class DrawRect(DrawCommand):
    x: float
    y: float
    width: float
    height: float
    color: Color

@dataclass
class DrawText(DrawCommand):
    x: float
    y: float
    text: str
    font_size: float
    color: Color

class Sizing: ...


class Fit(Sizing): ...


class Grow(Sizing): ...


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
    min_width: float = 0
    min_height: float = 0
    max_width: float = 0
    max_height: float = 0

class UIElement:
    def __init__(self) -> None:
        self.parent: 'UI' = UI.current_element[-1] if len(UI.current_element) != 0 else None
        if self.parent is not None and isinstance(self.parent, UI):
            self.parent.children.append(self)
        self.element_data = ElementData()

    def get_length_across(self, x_axis: bool) -> float:
        return self.element_data.width if x_axis else self.element_data.height

    def get_length_perpen(self, x_axis: bool) -> float:
        return self.get_length_across(not x_axis)

    def get_min_length_across(self, x_axis: bool) -> float:
        return self.element_data.min_width if x_axis else self.element_data.min_height

    def get_min_length_perpen(self, x_axis: bool) -> float:
        return self.get_min_length_across(not x_axis)

    def get_max_length_across(self, x_axis: bool) -> float:
        return self.element_data.max_width if x_axis else self.element_data.max_height

    def get_max_length_perpen(self, x_axis: bool) -> float:
        return self.get_max_length_across(not x_axis)

    def set_length_across(self, x_axis: bool, length: float) -> None:
        if x_axis:
            self.element_data.width = length
        else:
            self.element_data.height = length

    def set_length_perpen(self, x_axis: bool, length: float) -> float:
        self.set_length_across(not x_axis, length)

    def set_min_length_across(self, x_axis: bool, length: float) -> None:
        if x_axis:
            self.element_data.min_width = length
        else:
            self.element_data.min_height = length

    def set_min_length_perpen(self, x_axis: bool, length: float) -> float:
        self.set_min_length_across(not x_axis, length)

    def set_max_length_across(self, x_axis: bool, length: float) -> None:
        if x_axis:
            self.element_data.max_width = length
        else:
            self.element_data.max_height = length

    def set_max_length_perpen(self, x_axis: bool, length: float) -> float:
        self.set_max_length_across(not x_axis, length)

    def render(self, draw_commands: list['DrawCommand'] | None = None, x: float = 0, y: float = 0) -> list['DrawCommand']:
        ...

    def wrap_text(self) -> None:
        ...

class UI(UIElement):
    current_element: list['UI'] = []
    root_element: 'UI' = None
    text_measurer: TextMeasurer = None

    @staticmethod
    def set_text_measurer(text_measurer: TextMeasurer) -> None:
        UI.text_measurer = text_measurer

    def get_ui_length_across(self, x_axis: bool) -> Sizing:
        return self.ui_data.width if x_axis else self.ui_data.height

    def get_ui_length_perpen(self, x_axis: bool) -> Sizing:
        return self.get_ui_length_across(not x_axis)

    def get_padding_across(self, x_axis: bool) -> float:
        return self.ui_data.padding_left + self.ui_data.padding_right if x_axis else self.ui_data.padding_top + self.ui_data.padding_bottom

    def get_padding_perpen(self, x_axis: bool) -> float:
        return self.get_padding_across(not x_axis)

    def x_axis(self) -> bool:
        return isinstance(self.ui_data.layout_direction, LeftToRight)

    def __init__(self):
        super().__init__()
        self.ui_data = UIData()
        self.children: list['UI'] = []

    def __enter__(self) -> 'UI':
        return self.__open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__exit()

    def __open(self) -> 'UI':
        if len(UI.current_element) == 0:
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

    def handle_fit_sizing(self, x_axis: bool) -> None:
        for child in self.children:
            if isinstance(child, UI):
                child.handle_fit_sizing(x_axis)
        self.add_dimensions_to_parent(x_axis)

    def add_dimensions_to_parent(self, x_axis: bool) -> None:
        if self.parent is None:
            return
        parent_x_axis = self.parent.x_axis()
        if x_axis and not isinstance(self.parent.get_ui_length_across(parent_x_axis), Fixed):
            self.parent.set_length_across(
                parent_x_axis,
                self.parent.get_length_across(parent_x_axis) + self.get_length_across(parent_x_axis)
            )
            self.parent.set_min_length_across(
                parent_x_axis,
                self.parent.get_length_across(parent_x_axis) + self.get_length_across(parent_x_axis)
            )
        if not x_axis and not isinstance(self.parent.get_ui_length_perpen(parent_x_axis), Fixed):
            self.parent.set_length_perpen(
                parent_x_axis,
                max(self.parent.get_padding_perpen(parent_x_axis), self.get_length_perpen(parent_x_axis))
            )
            self.parent.set_min_length_across(
                parent_x_axis,
                self.parent.get_length_across(parent_x_axis) + self.get_length_across(parent_x_axis)
            )

    def __exit(self) -> 'UI':
        UI.current_element.pop()

        if isinstance(self.ui_data.width, Fixed):
            self.element_data.width += self.ui_data.width.pixels
        if isinstance(self.ui_data.height, Fixed):
            self.element_data.height += self.ui_data.height.pixels

        self.__add_padding_to_dimensions()

        return self

    def show(self) -> 'UI':
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

    def width_grow(self) -> 'UI':
        return self.width(Grow())

    def height_grow(self) -> 'UI':
        return self.height(Grow())

    def sizing_grow(self) -> 'UI':
        return self.width_grow().height_grow()

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

    def handle_growing_and_shrinking(self, x_axis: bool) -> None:
        if len(self.children) == 0:
            return

        if x_axis != self.x_axis():
            for child in self.children:
                child.handle_growing_and_shrinking(x_axis)
                if not (isinstance(child, Text) or isinstance(child.get_ui_length_across(x_axis), Grow)):
                    continue
                child.set_length_across(x_axis, self.get_length_across(x_axis) - self.get_padding_across(x_axis))
            return

        remaining_length = self.get_length_across(x_axis) - self.get_padding_across(x_axis)
        changeable: list[UI] = []
        for child in self.children:
            remaining_length -= child.get_length_across(x_axis)
            if isinstance(child, Text) or isinstance(child.get_ui_length_across(x_axis), Grow):
                changeable.append(child)
        remaining_length -= (len(self.children) - 1) * self.ui_data.child_gap

        while remaining_length > 0 and len(changeable) != 0: # grow
            smallest = changeable[0].get_length_across(x_axis)
            second_smallest = float('inf')
            length_to_add = remaining_length

            for child in changeable:
                if child.get_length_across(x_axis) < smallest:
                    second_smallest = smallest
                    smallest = child.get_length_across(x_axis)
                if child.get_length_across(x_axis) > smallest:
                    second_smallest = min(second_smallest, child.get_length_across(x_axis))
                    length_to_add = second_smallest - smallest

            length_to_add = min(length_to_add, remaining_length / len(changeable))

            for child in changeable:
                previous_length = child.get_length_across(x_axis)
                if child.get_length_across(x_axis) != smallest:
                    continue
                child.set_length_across(x_axis, child.get_length_across(x_axis) + length_to_add)
                if child.get_length_across(x_axis) >= (m := child.get_max_length_across(x_axis)) and m != 0:
                    child.set_length_across(x_axis, m)
                    changeable.remove(child)
                remaining_length -= child.get_length_across(x_axis) - previous_length

        while remaining_length < 0 and len(changeable) != 0: # shrink
            largest = changeable[0].get_length_across(x_axis)
            second_largest = 0
            length_to_add = remaining_length

            for child in changeable:
                if child.get_length_across(x_axis) > largest:
                    second_largest = largest
                    largest = child.get_length_across(x_axis)
                if child.get_length_across(x_axis) < largest:
                    second_largest = max(second_largest, child.get_length_across(x_axis))
                    length_to_add = second_largest - largest

            length_to_add = max(length_to_add, remaining_length / len(changeable))

            for child in changeable:
                previous_length = child.get_length_across(x_axis)
                if child.get_length_across(x_axis) != largest:
                    continue
                child.set_length_across(x_axis, child.get_length_across(x_axis) + length_to_add)
                if child.get_length_across(x_axis) <= (m := child.get_min_length_across(x_axis)):
                    child.set_length_across(x_axis, m)
                    changeable.remove(child)
                remaining_length += child.get_length_across(x_axis) - previous_length

        for child in self.children:
            if isinstance(child, UI):
                child.handle_growing_and_shrinking(x_axis)

    def wrap_text(self) -> None:
        for child in self.children:
            child.wrap_text()

@dataclass
class TextUIData:
    color: Color
    font_size: float = 5

class Text(UI):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.ui_data = TextUIData(Color(0, 0, 0))

    def font_size(self, font_size: float) -> 'Text':
        self.ui_data.font_size = font_size
        return self

    def color(self, color: Color) -> 'Text':
        self.ui_data.color = color
        return self

    def show(self) -> None:
        self.element_data.width = UI.text_measurer.get_text_width(self.text, self.ui_data.font_size)
        self.element_data.max_width = self.element_data.width
        self.element_data.height = UI.text_measurer.get_text_height(self.ui_data.font_size)
        self.element_data.min_height = self.element_data.height
        words = self.text.split(' ')
        if len(words) != 0:
            min_word_length = min(map(lambda s: UI.text_measurer.get_text_width(s, self.ui_data.font_size), words))
            self.element_data.min_width = min_word_length

    def wrap_text(self) -> None:
        if isinstance(self.parent.ui_data.height, Fit):
            if not self.parent.x_axis():
                self.parent.element_data.height += self.element_data.height
            else:
                inner_height = self.parent.element_data.height - (p := self.parent.get_padding_across(True))
                self.parent.element_data.height = max(inner_height, self.element_data.height) + p

    def render(self, draw_commands: list['DrawCommand'] | None = None, x: float = 0, y: float = 0) -> list['DrawCommand']:
        if draw_commands is None:
            draw_commands = []

        draw_commands.append(DrawText(
            x=x,
            y=y,
            text=self.text,
            font_size=self.ui_data.font_size,
            color=self.ui_data.color,
        ))

        return draw_commands

def render(x: float = 0, y: float = 0) -> list['DrawCommand']:
    root = UI.root_element

    root.handle_fit_sizing(True)
    root.handle_fit_sizing(False)
    root.handle_growing_and_shrinking(True)
    root.wrap_text()
    root.handle_growing_and_shrinking(False)

    return root.render(x=x, y=y)
