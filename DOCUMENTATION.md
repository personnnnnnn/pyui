*NOTE*: This documentation will probably become out of date as I
work on PyLay, but I'll try to document the changes made as I go.

# The Basics

PyLay is an ***immediate-mode*** UI library.

This means that the UI tree is rebuilt every
frame instead of being modified, unlike **retained-mode**
UIs, like *HTML*.

This, in practice, leads to an easier time overall because
state is no longer a problem; it literally does not exist.

Also, because PyLay returns a list of draw commands and doesnt just
draw to the screen directly, you can just make a custom renderer
and bring OyLay to your favourite python graphics library.

So far, this is literally just Clay, but in python instead of C.

But unlike Clay, where to specify the padding you have
to specify all the attributes separately (left, right, top and bottom padding),
like `{ .padding = { 32, 32, 32, 32 } }`, PyLay just has a method for the `UI` class named `padding()`
that just calls `padding_ver()` and `padding_hor()` which themselves call `padding_left()`,
`padding_right()`, and so on...

> There is also `spacing()` which calls `padding()` and `child_gap()`

This also means that you will have really long lines:
```python
with UI().background(Color(255, 255, 255)).sizing_fixed(screen.get_width(), screen.get_height()).padding(20).child_gap(10).top_to_bottom(): ...
```
... but unlike tailwind, we can just place the method calls on multiple lines like this:
```python
with (
    UI()
            .background(Color(255, 255, 255))
            .sizing_fixed(screen.get_width(), screen.get_height())
            .padding(20)
            .child_gap(10)
            .top_to_bottom()
): ...
```
... or even before the `with` block if you like (though this is a little more verbose)
```python
root_element = UI()
root_element.background(Color(255, 255, 255))
root_element.sizing_fixed(screen.get_width(), screen.get_height())
root_element.padding(20)
root_element.child_gap(10)
root_element.top_to_bottom()
with root_element:
    ...
```

# The `Color` Class

This is an object representing a color.

It has attributes `r`, `g` and `b` of type `int` representing the 3 color channels.

The constructor takes in three arguments corresponding to the 3 attributes.

# The `Sizing` Class

Is the input to the `UI.width()` and `UI.height()` functions.
It has 3 child classes specifying the sizing modes:

- `Fixed`: Takes in one argument -- the length in pixels.
- `Fit`: Takes in no arguments -- makes the container fit to the size of it's contents. It's also the default sizing option.
- `Grow`: Takes in no arguments -- makes the container grow to the size of it's parent, taking up all the space it can.
> If there are multiple grow containers in a single line, the remaining space will get distributed equally.

# The `LayoutDirection` Class

It is the input to the `UI.layout_direction()` function.
It has 2 child classes specifying the direction in which the child elements of a container are arranged:

- `LeftToRight` (default)
- `TopToBottom`

# The `UI` Class

> While there are some methods are omitted here, they are only used internally
> and descriptive of their purpose (the methods described by the documentation
> are too, but those are more important).

`UI` is the `div` of PyLay.

### `UI.show() -> None`
Equivalent to `with element: ...`

### `UI.background(color: Color | None) -> UI`
Sets the background of the element. If `color` is `None`, removes it instead.

### `UI.no_background() -> UI`
Removes the background.

Equivalent to `element.background(None)`

### `UI.padding_left(padding: float) -> UI`
Sets the left padding of a div in pixels.

### `UI.padding_right(padding: float) -> UI`
Sets the right padding of a div in pixels.

### `UI.padding_top(padding: float) -> UI`
Sets the top padding of a div in pixels.

### `UI.padding_bottom(padding: float) -> UI`
Sets the bottom padding of a div in pixels.

### `UI.padding_ver(padding: float) -> UI`
Sets the vertical padding of a div in pixels.

### `UI.padding_hor(padding: float) -> UI`
Sets the horizontal padding of a div in pixels.

### `UI.padding(padding: float) -> UI`
Sets the padding of all sides of a div in pixels.

### `UI.no_padding() -> UI`
Removes all padding.

Equivalent to `element.padding(0)`.

### `UI.child_gap(child_gap: float) -> UI`
Specifies the space to put in between the children of a div in pixels.

### `UI.no_child_gap() -> UI`
Removes all child gap.

Equivalent to `element.child_gap(0)`

### `UI.spacing(spacing: float) -> UI`
Sets the padding and child gap of a div in pixels.

### `UI.no_spacing() -> UI`
Removes all spacing.

Equivalent to `element.spacing(0)`

### `UI.width(sizing: Sizing) -> UI`
Sets the width.

### `UI.height(sizing: Sizing) -> UI`
Sets the height.

### `UI.width_fit() -> UI`
Set the width to be `Fit`.

Equivalent to `element.width(Fit())`.

### `UI.height_fit() -> UI`
Set the height to be `Fit`.

Equivalent to `element.height(Fit())`.

### `UI.sizing_fit() -> UI`
Sets the width and height to be `Fit`.

Equivalent to `element.width_fit().height_fit()`.

### `UI.width_grow() -> UI`
Set the width to be `Grow`.

Equivalent to `element.width(Grow())`.

### `UI.height_grow() -> UI`
Set the height to be `Grow`.

Equivalent to `element.height(Grow())`.

### `UI.sizing_grow() -> UI`
Sets the width and height to be `Grow`.

Equivalent to `element.width_grow().height_grow()`.

### `UI.width_fixed(width: float) -> UI`
Set the width to the amount specified in pixels.

Equivalent to `element.width(Fixed(width))`.

### `UI.height_fixed(height: float) -> UI`
Set the height to the amount specified in pixels.

Equivalent to `element.height(Fixed(height))`.

### `UI.sizing_fixed(width: float, height: float) -> UI`
Sets the width and height to be the specified dimensions in pixels.

Equivalent to `element.width_fixed(width).height_fixed(height)`.

### `UI.layout_direction(direction: LayoutDirection) -> UI`
Sets the direction in which the children of the container
are placed.

The default value is `LeftToRight`

### `UI.left_to_right() -> UI`
Sets the layout direction to `LeftToRight`

Equivalent to `element.layout_direction(LeftToRight())`

### `UI.top_to_bottom() -> UI`
Sets the layout direction to `TopToBottom`

Equivalent to `element.layout_direction(TopToBottom())`

# The `render` Function
### `render(x: float = 0, y: float = 0) -> list[DrawCommand]`







