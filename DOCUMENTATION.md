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

# The `UI` Class

`UI` is the `div` of PyLay.
It can have children and different styles applied to it to do anything you want.

## `UI.background(color: Color | None) -> UI`
Sets the background of the element. If `color` is `None`, removes it instead.

## `UI.no_background() -> UI`
Removes the background













