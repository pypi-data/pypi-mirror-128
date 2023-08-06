'''
Functions to manipulate widgets and other objects, that make no sense to be
used externally.

If useful, they should be exposed as methods.
'''
import logging
import typing
import sys
import math
from functools import wraps

import tkinter as tk  # Only for typechecking and asserts

from . import model
if typing.TYPE_CHECKING:
    from . import mixin


logger = logging.getLogger(__name__)


def label_size(chars: int) -> int:
    '''Estimate a label size (in pixels) by counting the number of chars.'''
    # TODO: Measure the font size: https://stackoverflow.com/a/30952406
    return math.ceil(-4 + 6 * math.pow(chars, 0.41))


def grid_size(*widgets: 'mixin.MixinWidget') -> 'model.GridSize':
    """Get the grid size for the given widgets.

    This should be used by a frame to calculate its grid size,
    by checking the values for all its children widgets.

    Args:
        widgets: Widgets in the same grid. There should be at least one.
    """
    def maxs(w):
        assert isinstance(w, tk.Widget), f'Invalid Widget: {w!r}'
        info = w.grid_info()
        # logger.debug(f'=> Grid Info: {info}')
        # If the grid information doesn't exist, default to a single frame
        # Force elements to integer, on tcl v8.5 they are returned as strings
        r = int(info.get('row', 0)) + int(info.get('rowspan', 1)) - 1
        c = int(info.get('column', 0)) + int(info.get('columnspan', 1)) - 1
        return (r, c)
    if __debug__:
        parents = set()
        for w in widgets:
            if w.wparent:
                parents.add(w.wparent)
        assert len(parents) == 1, f'Grid Size only for sibling widgets. Parents {parents}'
    m = [maxs(w) for w in widgets]
    num_columns = max([w[1] for w in m]) + 1
    num_rows = max([w[0] for w in m]) + 1
    return model.GridSize(rows=num_rows, columns=num_columns)


def configure_grid(master: 'mixin.ContainerWidget', column_weights: typing.Sequence[int], row_weights: typing.Sequence[int], **kwargs) -> None:
    """Configure the grid.

    Weights can be:

        - ``0`` : Fit the widgets, never resize
        - ``>0``: Resize with this number as weight

    Make sure to include all columns and rows. When in doubt, use 0

    Args:
        column_weights: List of column weights
        row_weights: List of row weights
        kwargs: Extra arguments to `columnconfigure
            <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M8>`_/`rowconfigure
            <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M24>`_ function.
    """
    if __debug__:
        gw = master.gsize
        gr = model.GridSize(rows=len(row_weights), columns=len(column_weights))
        assert gw == gr, f'{master!r}: Invalid grid size: W::{gw} R::{gr}'
    assert isinstance(master, (tk.Widget, tk.Tk)), f'{master} is not a valid tkinter.Widget'
    for col, w in enumerate(column_weights):
        master.columnconfigure(col, weight=w, **kwargs)
    for row, h in enumerate(row_weights):
        master.rowconfigure(row, weight=h, **kwargs)


def generate_trace(variable: tk.Variable, function: typing.Callable, **kwargs):
    '''Generate an internal trace callback.

    The function generated here should be attached to the ``Tk`` event.
    '''
    @wraps(function)
    def wrapper(name: str, index: typing.Any, etype: model.TraceModeT):  # "Real" tk function
        assert isinstance(name, str) and isinstance(etype, str)
        return function(variable, etype, **kwargs)
    return wrapper


def vname(variable: tk.Variable) -> str:
    '''Collect the variable name.

    This is set on the object, but there's no typing support for it. Double check it here.
    '''
    assert hasattr(variable, '_name'), 'tk.Variable has changed the implementation'
    return variable._name  # type: ignore


def bind_mousewheel(widget, up: typing.Callable, down: typing.Callable, **kwargs) -> typing.Union[model.Binding, typing.Tuple[model.Binding, model.Binding]]:
    '''OS-independent mouse wheel bindings.

    This is a digital scroll.

    On Linux, this is implemented as two special mouse buttons ("up" and
    "down". Windows supports analog mouse wheels, but this function emulates a
    digital scroll out of that.

    The return value is platform-specific:

    - On Linux, return the two `Binding` object, for "up" and "down" mouse
      scroll.

    - On Windows, returns the single `Binding` object for the analog mouse
      scroll.

    Note:
        This uses regular `Binding` objects, remember that ``immediate=True``
        is needed to activate the binding on start.
    '''
    if sys.platform == 'linux':
        bup = model.Binding(widget, '<Button-4>', up, **kwargs)
        bdown = model.Binding(widget, '<Button-5>', down, **kwargs)
        return bup, bdown
    elif sys.platform == 'win32':
        def wrap_scroll(event):
            if event.delta > 0:
                return up(event)
            elif event.delta < 0:
                return down(event)
            else:
                raise NotImplementedError
        binding = model.Binding(widget, '<MouseWheel>', wrap_scroll, **kwargs)
        return binding
    else:
        logger.critical(f'Unsupported system platform: {sys.platform}')
        return NotImplementedError
