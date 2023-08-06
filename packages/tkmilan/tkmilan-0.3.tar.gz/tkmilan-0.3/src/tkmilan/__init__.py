#!/usr/bin/env python
"""
`tkinter`'s evil twin.
"""
import typing
import logging
import warnings
from contextlib import contextmanager
from dataclasses import dataclass

import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog  # Implemented in newer typshed versions

from . import model
from . import var
from . import mixin
from . import exception
from . import spec
from . import parser
from . import fn


MODULES_VERBOSE = (
    'mixin.layout',
    'model.layout',
)
'''Shows spammy modules, should be silenced by the calling application.

These sub-modules sent enormous amount of logs, bordering on spam, on the
``logging.DEBUG`` setting.

The calling application should use something like this to silence them:

.. code:: python

    if loglevel == logging.DEBUG:
        for dmodule in MODULES_VERBOSE:
            logging.getLogger(f'tkmilan.{dmodule}').setLevel(logging.INFO)
'''


# TypeChecking
class varTree(var.ObjectList[model.TreeElement]):
    '''Type-Checking variable type for `Tree`.'''
    pass


# Useful models
Binding = model.Binding

# Layouts
# TODO: Transform into a `enum.Enum`?
AUTO = mixin.AUTO
'''Automatic Layout.
'''
HORIZONTAL = mixin.HORIZONTAL
'''Horizontal (1 row) Layout.
'''
VERTICAL = mixin.VERTICAL
'''Vertical (1 column) Layout.
'''

logger = logging.getLogger(__name__)


# Usable Widgets


class RootWindow(tk.Tk, mixin.ContainerWidget):
    '''A root window, the toplevel widget for the entire application.

    Usually there's only one of this in a single application. Multiple root
    windows are unsupported.

    See `tkinter.Tk`.

    Args:
        theme: Theme to use. Default to choosing a tasteful choice depending on
            the OS.

    Note:
        Technically, it should be OK to use multiple root windows per-process,
        but this hasn't been tested, there are no test cases where this makes
        sense.
    '''
    isNoneable: bool = False  # Always present, no matter what

    def __init__(self, *args, theme: str = None, **kwargs):
        self._bindings_global: typing.MutableMapping[str, model.BindingGlobal] = {}
        super().__init__()  # tk.Tk
        kwargs['expand'] = False  # `Toplevel` has no parent grid to expand
        self.init_container(*args, **kwargs)
        self.style = self.setup_style(theme)

    def setup_style(self, theme: typing.Optional[str]) -> ttk.Style:
        style = ttk.Style(self)
        if theme is None:
            # Good for Linux
            # On Windows, check: 'winnative', 'vista'
            theme = 'alt'
        style.theme_use(theme)
        return style

    def instate(self, statespec: typing.Sequence[str], callback: typing.Optional[typing.Callable] = None) -> typing.Optional[bool]:
        ''''''  # Do not document
        # Not applicable to the root window
        return None

    def state(self, statespec):
        ''''''  # Do not document
        # Not applicable to root window
        raise NotImplementedError


class FrameUnlabelled(ttk.Frame, mixin.ContainerWidget):
    '''A simple frame to hold other widgets, visually invisible.

    This is the simplest form of `mixin.ContainerWidget`, just a bunch of
    widgets. There's no separation between the outside and the inside of the
    frame.

    There is no Python documentation, see ``Tk`` `ttk.Frame <https://www.tcl.tk/man/tcl/TkCmd/ttk_frame.html>`_ documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `FrameLabelled`: Visible version, with a label.
    '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)  # ttk.Frame
        self.init_container(*args, **kwargs)


class FrameLabelled(ttk.LabelFrame, mixin.ContainerWidget):
    '''A frame to hold other widgets surrounded by a line, including a label.

    This is a frame with a label. It is visually separated from the other
    widgets. You can control the label position.

    There is no Python documentation, see ``Tk`` `ttk.LabelFrame <https://www.tcl.tk/man/tcl/TkCmd/ttk_labelframe.html>`_ documentation.

    Args:
        label: The label to include on the frame separator. Can be given as a class variable.
        labelAnchor: The position of the label on the frame separator.
            Given as one of the cardinal points.
            Defaults to a OS-specific location (`model.CP.default`).

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `FrameUnlabelled`: Invisible version, without a label.

        `FrameStateful`: Support for an embedded `Checkbox` as label.
    '''
    label: typing.Optional[str] = None

    def __init__(self, parent, *args, label: typing.Optional[str] = None, labelAnchor: model.CP = model.CP.default, **kwargs):
        chosen_label = self.label or label
        if chosen_label is None:
            raise exception.InvalidWidgetDefinition('{self!r}: Missing required label')
        # TODO: Improve labelAnchor object
        super().__init__(parent, text=chosen_label, labelanchor=labelAnchor.value)  # ttk.LabelFrame
        if __debug__:
            if 'labelwidget' in kwargs:
                warnings.warn(f'{self}: Unsupported "labelwidget"', stacklevel=2)
        kwargs.pop('labelwidget', None)  # Unsupported
        self.init_container(*args, **kwargs)


class Label(ttk.Label, mixin.SingleWidget):
    '''A label, can be text, image, or both.

    This is a label, a static-ish widget without interaction.

    This must include at least some text or an image, even though both are optional.

    No state is included.

    There is no Python documentation, see ``Tk`` `ttk.Label <https://www.tcl.tk/man/tcl/TkCmd/ttk_label.html>`_ documentation.

    Args:
        label: The text to show. Optional. Can be given as a class variable.
        image: The image to show. Optional.
            See ``Tk`` `tk.Image <https://www.tcl.tk/man/tcl/TkCmd/image.html>`_ documentation.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
    '''
    label: typing.Optional[str] = None
    state_type = var.nothing

    def __init__(self, parent, *, label: typing.Optional[str] = None, image: typing.Optional[tk.Image] = None, **kwargs):
        # TODO: Support `anchor`, with `model.CP`
        chosen_label = self.label or label
        if chosen_label is None and image is None:
            raise exception.InvalidWidgetDefinition('{self!r}: Needs an image or a label')
        self.init_single(variable=None)  # No state here
        super().__init__(parent, **kwargs)  # ttk.Label
        assert isinstance(chosen_label, str)
        if chosen_label:
            self.set_label(chosen_label)
        if image:
            self.set_image(image)
        self.binding('<Button-1>', self.invoke_onClick)

    def invoke_onClick(self, event=None):
        ''''''  # Internal, do not document
        self.onClick()

    def set_image(self, image: tk.Image) -> None:
        '''Change the label image.'''
        self._image = image  # Save a reference to avoid garbage collection
        self['image'] = self._image

    def set_label(self, label: str) -> None:
        '''Change the label text.'''
        self['text'] = label

    # TODO: Pass the event object?
    # TODO: Not needed on labels
    def onClick(self):
        """Callback to be executed when clicking this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.
        """
        pass


class Button(ttk.Button, mixin.SingleWidget):
    '''A button with a label.

    This is a button, with a label. The main interaction is being clicked on.

    No state is included.

    There is no Python documentation, see ``Tk`` `ttk.Button <https://www.tcl.tk/man/tcl/TkCmd/ttk_button.html>`_ documentation.

    Args:
        label: The label to include inside the button. Optional. Can be given as a class variable.
        width: The button width, in pixels.
            Defaults to an ad-hoc calculation based on the length of the label.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
    '''
    label: typing.Optional[str] = None
    state_type = var.nothing

    def __init__(self, parent, *, label: typing.Optional[str] = None, width: typing.Optional[int] = None, **kwargs):
        chosen_label = self.label or label
        if chosen_label is None:
            raise exception.InvalidWidgetDefinition('{self!r}: Missing required label')
        self.init_single(variable=None)  # No state here
        assert isinstance(chosen_label, str)
        kwargs.update({
            'text': chosen_label,
            'width': width or fn.label_size(len(label or 'M')),
            'command': self.invoke_onClick,
        })
        super().__init__(parent, **kwargs)  # ttk.Button

    def invoke_onClick(self):
        ''''''  # Internal, do not document
        self.onClick()

    def onClick(self):
        """Callback to be called when clicking this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.
        """
        pass


class Checkbox(ttk.Checkbutton, mixin.SingleWidget):
    '''A checkbox, simple boolean choice.

    This is a checkbox with a label. The main interaction is being clicked on,
    which toggles its value.

    The state is a single `bool` value.

    There is no Python documentation, see ``Tk`` `ttk.Checkbutton <https://www.tcl.tk/man/tcl/TkCmd/ttk_checkbutton.htm>`_ documentation.

    Args:
        label: The label to include besides the checkbox. Can be given as a class variable.
            It is included on the right side of the checkbox.
        readonly: Should the widget allow interaction to toggle its value. Default to *allowing* interaction.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        variable: Use an externally defined variable, instead of creating a new one specific for this widget.
    '''
    label: typing.Optional[str] = None
    state_type = var.Boolean

    def __init__(self, parent, *, label: typing.Optional[str] = None, readonly: bool = False, variable: typing.Optional[var.Boolean] = None, **kwargs):
        chosen_label = self.label or label
        if chosen_label is None:
            raise exception.InvalidWidgetDefinition('{self!r}: Missing required label')
        self.init_single(variable, gkeys=['readonly'])
        assert isinstance(chosen_label, str)
        kwargs.update({
            'text': chosen_label,
            'onvalue': True,
            'offvalue': False,
            'variable': self.variable,
        })
        super().__init__(parent, **kwargs)  # ttk.Checkbutton
        if readonly:
            # Read-only checkboxen are editable, for some reason
            self.gstate = model.GuiState(enabled=False, readonly=True)

    def toggle(self) -> None:
        '''Switch the variable state to its opposite (`not <not>`).'''
        self.wstate = not self.wstate


class Entry(ttk.Entry, mixin.SingleWidget):
    '''An entry widget, single-line text editor.

    This is an entry box, a single-line editor for strings. The main
    interaction is editing the text contained within.

    The state is a single `str` value.

    There is no Python documentation, see ``Tk`` `ttk.Entry <https://www.tcl.tk/man/tcl/TkCmd/ttk_entry.htm>`_ documentation.

    Args:
        variable: Use an externally defined variable, instead of creating a new one specific for this widget.

        label: The label to include besides the entry. **Not implemented yet**.
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
    '''
    state_type = var.String

    def __init__(self, parent, *, variable: typing.Optional[var.String] = None, label: typing.Optional[str] = None, **kwargs):
        self.init_single(variable)
        self.label = label or ''  # TODO: Show label somehow?
        kwargs.update({
            'textvariable': self.variable,
        })
        super().__init__(parent, **kwargs)  # ttk.Entry
        if __debug__:
            if label is not None:
                warnings.warn(f'{self}: Labels on Entry are still unsupported. Include a Label manually.', stacklevel=2)


class Combobox(ttk.Combobox, mixin.SingleWidget):
    '''A combobox widget, combining an `Entry` with a `Listbox`.

    This is a combobox, an `Entry` with a button that shows a pop-up `Listbox`
    with some predefined ``values``.

    The entry can be ``readonly``, in which case the only possible values are
    the ones shown on the value list, otherwise the entry is editable with
    arbitrary values, just like any `Entry`.

    The ``immediate`` parameter can be used to control when is the default
    value setup. Defaults to being set only when the GUI stabilizes, but it can
    be set as soon as possible.

    There is no Python documentation, see ``Tk`` `ttk.Combobox <https://www.tcl.tk/man/tcl/TkCmd/ttk_combobox.html>`_ documentation.

    Args:
        values: A countable specification of values to show on the pop-up listbox.
        readonly: Should the widget allow interaction to change its value.
            Defaults to *disallowing* interaction.
        immediate: Set the default value ASAP (`True`), or delay it after the
            GUI is stable (`False`). Defaults to `False`.
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.

        label: The label to include besides the combobox. **Not implemented yet**.
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
    '''
    state_type = var.String

    def __init__(self, parent, values: spec.SpecCountable, *, readonly: bool = True, immediate: bool = False, variable: typing.Optional[var.String] = None, label: typing.Optional[str] = None, **kwargs):
        self.init_single(variable, gkeys=['readonly'])
        self.label = label or ''  # TODO: Show label somehow
        self.specValues = values
        kwargs.update({
            'textvariable': self.variable,
            'values': list(self.specValues.all()),
        })
        super().__init__(parent, **kwargs)  # ttk.Combobox
        if immediate:
            self.setDefault()
        else:
            self.after_idle(self.setDefault)  # No need for a `TimeoutIdle` here
        if readonly:
            self.gstate = model.GuiState(readonly=True)
        if __debug__:
            # Define all the local subclasses (that override __init__) to improve logging
            _deltalevel = 1 if isinstance(self, (ComboboxMap,)) else 0
            if not isinstance(self, ComboboxMap) and isinstance(self.specValues, spec.StaticMap):
                warnings.warn(f'{self}: See `ComboboxMap` for using the values correctly', stacklevel=2 + _deltalevel)
            if label is not None:
                warnings.warn(f'{self}: Labels on Combobox are still unsupported. Include a Label manually.', stacklevel=2 + _deltalevel)

    # TODO: This could be a common `mixin.SingleWidget` method?
    def setDefault(self) -> None:
        '''Set the current state to the default label.'''
        self.wstate = self.specValues.default

    # TODO: This could be a common `mixin.SingleWidget` method?
    def eSet(self, label: str) -> typing.Callable[..., None]:
        '''Return an event function to set the state a certain label.'''
        if label not in self.specValues:
            raise exception.InvalidCallbackDefinition(f'Setting an invalid label: {label}')

        def eSet():
            self.wstate = label
        return eSet


class ComboboxMap(Combobox):
    '''A combobox widget, prepared to use `spec.StaticMap`.

    This is just a normal `Combobox`, but the ``values`` object must be a
    `spec.StaticMap`, and the widget value will be returned as its value, not
    the label.

    Note:
        This is still WIP, seems like a very big hack for now.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(self.specValues, spec.StaticMap), f'{self}: values must be a `spec.StaticMap`'

    def state_get(self, *args, **kwargs):
        ''''''  # Do not document
        label = super().state_get(*args, **kwargs)
        value = self.specValues.value(label)
        # if __debug__:
        #     logger.debug('L[%s] => %r', label, value)
        return model.VState(value, label=label)

    def state_set(self, state, *args, **kwargs):
        ''''''  # Do not document
        # Support setting labels and VState
        if isinstance(state, model.VState):
            label = self.specValues.label(state.value)
            if __debug__:
                if state.label:
                    assert state.label == label
                # logger.debug('%r => %s', state, label)
        else:  # Setting a simple label
            label = state
            if __debug__:
                pass  # logger.debug('L[%s]', label)
        return super().state_set(label, *args, **kwargs)

    def eSetValue(self, value):
        '''Wraper for `Combobox.eSet`, prepared to use `spec.StaticMap`.'''
        assert isinstance(self.specValues, spec.StaticMap)
        return self.eSet(self.specValues.label(value))

    if __debug__:
        # Warn about trace usage
        def trace(self, *args, **kwargs):
            if self.specValues not in kwargs.values():
                warnings.warn('Make sure to send `self.specValues` to get the "real" values', stacklevel=2)
            return super().trace(*args, **kwargs)


class FrameStateful(ttk.LabelFrame, mixin.ContainerWidget):
    '''A frame to hold other widgets, with a checkbox.

    This is a frame with an embedded checkbox `cstate_widget` as "label". This
    label controls the enabled state of the child widgets. You can control the
    checkbox position.

    There is no Python documentation, see ``Tk`` `ttk.LabelFrame <https://www.tcl.tk/man/tcl/TkCmd/ttk_labelframe.html>`_ documentation.
    Note the ``labelwidget`` option.

    Args:
        label: The label to include on the frame separator. Can be given as a class variable.
        labelAnchor: The position of the label on the frame separator.
            Given as one of the cardinal points.
            Defaults to a OS-specific location (`model.CP.default`).
        cvariable: Use an externally defined `cstate` variable, instead of
            creating a new one specific for the `cstate` widget.
        cvariableDefault: The default value for `cstate`.
            When `None`, the value is not changed at start.
            Defaults to starting enabled, unless ``cvariable`` is given, for
            which the value is not changed.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `FrameLabelled`: A simpler version of this, without the embedded checkbox.
    '''
    label: typing.Optional[str] = None

    class __w_cstate(Checkbox):
        isHelper = True

    cstate_widget: __w_cstate
    '''The widget for the embedded `Checkbox`.

    Uses the `cstate` variable.

    Note:
        The widget type is a local `Checkbox` subclass, specific for this widget.
    '''
    cstate: var.Boolean
    '''The variable holding the embedded `Checkbox` state.

    Used on the `cstate_widget`.

    See Also:
        ``cvariable``: This can be configured as an external variable.
    '''

    def __init__(self, parent, *args, label: typing.Optional[str] = None, labelAnchor: model.CP = model.CP.default,
                 cvariable: typing.Optional[var.Boolean] = None, cvariableDefault: typing.Optional[bool] = None,
                 **kwargs):
        # Create the checkbox widget
        chosen_label = self.label or label
        if chosen_label is None:
            raise ValueError('{self!r}: Missing required label')
        # TODO: Support `cstateArgs`, to append arbitrary arguments?
        cstate_widget = self.__class__.__w_cstate(parent, label=chosen_label, readonly=False, variable=cvariable)
        assert isinstance(cstate_widget.variable, var.Boolean), f'{self!r} checkbox widget is not a simple boolean'
        self.cstate = cstate_widget.variable
        # Usual Initialization
        super().__init__(parent, labelwidget=cstate_widget, labelanchor=labelAnchor.value)
        self.init_container(*args, **kwargs)
        # Configure the checkbox widget
        self.cstate_widget = cstate_widget
        self.cstate_widget.trace(self.onChanged_cstate)
        # # Setup the default value for that widget
        if __debug__:
            if cvariable is not None and cvariableDefault is not None:
                warnings.warn(f'{self}: cvariable: Setting a default with an external variable')
        if cvariable is None and cvariableDefault is None:
            cvariableDefault = True
        if cvariableDefault is not None:
            self.cstate.set(cvariableDefault)

    def state_get(self, *args, **kwargs) -> model.WState[bool, typing.Any]:
        ''''''  # Do not document
        return model.WState(
            self.cstate.get(),
            super().state_get(*args, **kwargs),
        )

    def state_set(self, state: model.WState, *args, **kwargs):
        ''''''  # Do not document
        assert isinstance(state.state, bool), f'Invalid WState: {state!r}'
        self.cstate.set(state.state)
        super().state_set(state.substate, *args, **kwargs)

    def set_gui_state(self, state: typing.Optional[model.GuiState] = None, **kwargs) -> None:
        # "Trace" the frame enabled status
        frame_enabled = kwargs.get('enabled', None) if state is None else state.enabled
        super().set_gui_state(state, **kwargs)
        if isinstance(frame_enabled, bool):
            state_enabled = self.cstate.get()
            # if __debug__:
            #     logger.debug(f'S| {self}: F={frame_enabled} S={state_enabled}')
            self.cstate_widget.gstate = model.GuiState(enabled=frame_enabled)
            self.set_gui_substate(enabled=frame_enabled and state_enabled)
            # TODO: unsetOnDisable
            # TODO: setOnEnable

    def onChanged_cstate(self, cstate, etype):
        assert etype == 'write'
        status = cstate.get()
        frame_enabled = self.gstate.enabled
        # if __debug__:
        #     logger.debug(f'{self}: S={status} Fe={frame_enabled}')
        self.set_gui_substate(model.GuiState(enabled=frame_enabled and status))


# TODO: Use `tk.scrolledtext.ScrolledText`? Do the same thing for multiple widgets?
class EntryMultiline(tk.Text, mixin.SingleWidget):
    '''A multiline text widget, supporting `LTML` contents.

    This is a multiline version of the `Entry` widget, with rich text
    capabilities.
    Supports only the readonly state, that is, the widget contents can only be
    edited programatically.

    The state is a single `str` value, internally parsed to `parser.LTML
    <LTML>`.

    There is no Python documentation, see ``Tk`` `tk.Text <https://www.tcl.tk/man/tcl/TkCmd/text.htm>`_ documentation.

    Args:
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.
        style: Configure the widget style.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    Note:

        The underlying widget is not part of `ttk <tkinter.ttk>` like most others. All
        efforts are expended to make this an implementation detail, without
        practical effects.
    '''
    state_type = var.String

    @dataclass
    class Style(model.WStyle):
        '''`EntryMultiline` style object.

        These are the colours:

        Args:
            colour_bg_on: Widget background, when enabled.
            colour_bg_off: Widget background, when disabled.
            colour_link_normal: Hyperlink foreground colour, normal links.
            colour_link_visited: Hyperlink foreground colour, visited links.
        '''
        colour_bg_on: str = 'white'
        colour_bg_off: str = 'lightgrey'
        colour_link_normal: str = 'blue'
        colour_link_visited: str = 'purple'

    def __init__(self, parent, *, variable: var.String = None,
                 style: Style = Style(_default=True),
                 **kwargs):
        self.wstyle = style
        self.init_single(variable)
        kwargs.pop('state', None)  # Support only readonly state
        super().__init__(parent, **kwargs)  # tk.Entry
        readonly = True  # Support only readonly state, for now...
        # GUI State Tracker
        # - Since this is not a `ttk.Widget`, this need to be emulated
        self.__gstate: model.GuiState = model.GuiState(enabled=True, readonly=readonly)
        assert self.variable is not None, f'{self!r}: Missing variable'
        self.wstate = getattr(self.variable, '_default', '')  # Set the default (before the trace)
        # State Tracker
        self.trace(self._varChanged, trace_name=f'__:{__name__}')

        # Bindings
        # TODO: Investigate changing the cursor on mouseover
        # TODO: Support `BindingTag`(`self.binding_tag`)?
        self.tag_bind('a', '<Button-1>', self._onClickTag, add=True)
        if readonly:
            self.binding('<Double-Button-1>', lambda e: 'break')  # Disable double click

    def _varChanged(self, var, etype):
        assert etype == 'write'
        # This function is called when the value changes
        # It's the implementation that binds the variable and the widget,
        #  so this should be idempotent
        vs = var.get()
        with self.as_editable():
            # Delete the entire state
            # From: First line, first character
            #   To: End
            self.delete('1.0', 'end')
            # Reset styles
            self.style_reset()
            # Add the current state
            # TODO: Save the TextElement somewhere in this object, with `data`?
            for te in parser.parse_LTML(vs):
                assert isinstance(te, model.TextElement)
                self.insert(tk.END, te.text, te.atags)

    def get_gui_state(self) -> model.GuiState:
        ''''''  # Do not document
        if __debug__:
            logger.debug('State > %r', self.__gstate)
        # return a copy of the object
        return model.GuiState(**dict(self.__gstate.items()))

    def set_gui_state(self, state: typing.Optional[model.GuiState] = None, *, _internal: bool = False, **kwargs) -> None:
        ''''''  # Do not document
        if state is None:
            state = model.GuiState(**kwargs)
        # if __debug__:
        #     logger.debug('State < %r', state)
        # Adjust current state
        for sname, svalue in state.items():
            assert sname != '_internal'  # Should be impossible...
            if svalue is not None:
                if sname == 'readonly' and _internal is False:
                    raise ValueError(f'{self}: No support for external readonly state manipulation')
                setattr(self.__gstate, sname, svalue)
        # Adjust widget state
        cfg = {}
        if self.__gstate.enabled is True:
            if self.__gstate.readonly is not None:
                cfg['state'] = tk.NORMAL if not self.__gstate.readonly else tk.DISABLED
            cfg['background'] = self.wstyle.colour_bg_on
        elif self.__gstate.enabled is False:
            cfg['state'] = tk.DISABLED
            cfg['background'] = self.wstyle.colour_bg_off
            self.style_reset()
        # if __debug__:
        #     logger.debug('C %s', self.__gstate)
        #     logger.debug('| %s', cfg)
        self.configure(**cfg)
        # Valid: TBD

    @contextmanager
    def as_editable(self):
        '''Temporarily mark the widget as editable.

        A context manager, used to change the contents of the widget while keep
        it "readonly".
        Technically, this should only be used internally, using the state
        tracker functions, but it might be useful externally.

        This is to be used like this:

        .. code:: python

            # `widget` is readonly
            with widget.as_editable():
                pass  # `widget` is editable
            # `widget` is readonly
        '''
        assert self.__gstate.readonly is True
        self.set_gui_state(readonly=False, _internal=True)
        try:
            yield
        finally:
            self.set_gui_state(readonly=True, _internal=True)

    def _style_a(self, tag: str = 'a', *, visited: bool) -> None:
        fg = self.wstyle.colour_link_visited if visited else self.wstyle.colour_link_normal
        self.tag_configure(tag, foreground=fg, underline=True)

    def style_reset(self, event=None, *, a: bool = True) -> None:
        '''Reset the style to the original.

        Args:
            a: Reset ``a`` anchors.

            event: Optional, unused. This exists for API compatibility with the
                ``onClick`` functions.
        '''
        for tag in self.tag_names():
            # a
            if a and tag == 'a' or tag.startswith('a::'):
                self._style_a(tag=tag, visited=False)

    def _onClickTag(self, event, *, tag_name: str = 'a'):
        if not self.__gstate.enabled:
            return  # Do nothing when disabled
        dobj = self.dump(f'@{event.x},{event.y}', text=True, tag=True)
        if __debug__:
            logger.debug('D: %r', dobj)
        dwhat = [dinner[0] for dinner in dobj]
        tags_cl = []  # Ignore the "sel" tag
        if 'tagon' in dwhat:
            # Click in the start of the tag
            tags_cl = [lst[1] for lst in dobj if lst[0] == 'tagon' and lst[1] != tk.SEL]
            # For nested tags, this might not be the same as the text method
        if len(tags_cl) == 0 and 'text' in dwhat:
            # Click in the middle of the tag
            click_location = [lst[2] for lst in dobj if lst[0] == 'text'][0]
            tp = self.tag_prevrange(tag_name, click_location)
            if __debug__:
                logger.debug(' | Text @ <%s', tp)
            tags_cl = [lst[1] for lst in self.dump(*tp, tag=True) if lst[1] != tk.SEL]
        if len(tags_cl) == 0:
            raise NotImplementedError
        if __debug__:
            logger.debug(' | Tags %s', tags_cl)
        assert len(tags_cl) >= 2, f'Missing tags: {tags_cl}'
        tags_proc = [t for t in tags_cl if '::' in t]
        assert len(tags_proc) == 1
        tagi = tags_proc[0]
        tag = tagi.split('::')[0]
        assert tag_name == tag, f'Wrong onClickTag: Requested[{tag_name}] != Found[{tag}]'
        assert tag in tags_cl, f'Wrong tag_index: {tag}[{tagi}]'
        tags_other = [t for t in tags_cl if t not in (tag, tagi)]
        if __debug__:
            logger.debug(f' = {tag}[{tagi}]')
        self._style_a(tag=tagi, visited=True)
        self.onClickTag(tag, tagi, tags_other)

    def onClickTag(self, tag: str, tag_index: str, tags_other: typing.Sequence[str]) -> None:
        """Callback to be called when clicking ``a`` tags in this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.

        Args:
            tag: The main tag type. In this case, it's always ``a``.
            tag_index: The tag index. See `LTML <parser.LTML>` Automatic Counter tags.
            tags_other: List of extra tags attached to the anchor. Might be empty.
        """
        pass


class Notebook(ttk.Notebook, mixin.ContainerWidget):
    '''A tabbed interface to hold other containers.

    This is a tabbed interface to show several containers in the same space.

    The individual tabs must all be containers, there's no support for single
    widgets. Use a holder `FrameUnlabelled` to show a single widget for each
    tab.

    There is no Python documentation, see ``Tk`` `ttk.Notebook <https://www.tcl.tk/man/tcl/TkCmd/ttk_notebook.html>`_ documentation.

    Args:
        traversal: Setup tab traversal with special keyboard shortcuts, and
            also with mouse wheel scrolling. See the Tk documentation for the
            keyboard part. Enabled by default.
        traversalWraparound: When ``traversal`` is setup, configure wraparound.
            That is, scrolling to the next tab from the last one should "scroll"
            into the first tab, and vice-versa for the first tab. This only matters
            for the mouse wheel traversal, the keyboard shortcuts always enable
            this traversal.
            Disabled by default.

        layout: Ignored, it is hardcoded to `None` always.
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `NotebookUniform`: A simpler version of this, when each individual tab is the same type
    '''
    Tab = model.NotebookTab  # Alias the notebook tab information  # TODO: Move NotebookTab class here?
    '''Alias for `model.NotebookTab` class.'''
    wtabs: typing.Mapping[str, model.NotebookTab]
    '''Mapping of tab identifiers, and `model.NotebookTab` objects.'''

    def __init__(self, parent, *args, layout: None = None, traversal: bool = True, traversalWraparound: bool = False, **kwargs):
        super().__init__(parent)
        # No `layout` is used, force it to `None`
        self.init_container(*args, layout=None, **kwargs)
        # Tab Traversal
        self.tWraparound = traversalWraparound
        if traversal:
            # TODO: Re-Implement locally, take `traversalWraparound` into account.
            #       Map:
            #       - `Ctrl-Tab`: _tabScrollUp
            #       - `Ctrl-Shift-Tab`: _tabScrollDown
            self.enable_traversal()
            # Bind mouse wheel: Digital Scrolling
            self._traversal = fn.bind_mousewheel(self, up=self._tabScrollUp, down=self._tabScrollDown, immediate=True)

    def setup_widgets(self, *args, **kwargs):
        '''Define the sub widgets based on the tabs.

        Do not overwrite this unless you know what you are doing.

        To edit the tabs, see `setup_tabs`.
        '''
        self.wtabs = self.setup_tabs(*args, **kwargs)
        # if __debug__:
        #     logger.debug(f'{self}: {len(self.wtabs)} Tabs')
        widgets = {}
        for identifier, ti in self.wtabs.items():
            # if __debug__:
            #     logger.debug('> %s: %r', ti.name, ti.widget)
            assert isinstance(ti.widget, mixin.ContainerWidget), f'{self!r}: Tab Widget [{ti.identifier or identifier}]"{ti.name}" must be a container'
            extra = {
                **ti.extra,
                'text': ti.name,
                'image': ti.image or '',
                'compound': ti.imageCompound,
            }
            self.add(ti.widget, **extra)
            ti.identifier = identifier
            widgets[identifier] = ti.widget
        return widgets

    def setup_tabs(self, *args, **kwargs) -> typing.Mapping[str, model.NotebookTab]:
        '''Define the tabs here.

        Similar to `setup_widgets <mixin.ContainerWidget.setup_widgets>`, but
        defines `model.NotebookTab`, extra information about each widget.
        '''
        raise NotImplementedError

    def wselection(self) -> str:
        '''Search for the current selected tab.

        Returns:
            This functions searches for the currently selected tab, and returns its
            identifier (the key on the `wtabs` dictionary).
        '''
        # TODO: Optimise this? Save a dict of indexes or something?
        selected_id = self.select()
        if __debug__:
            logger.debug('S: %r', selected_id)
            tabs_id = [str(w) for w in self.tabs()]
            logger.debug(' | %s', ' '.join(tabs_id))
        for idx, wtab in self.wtabs.items():
            if str(wtab.widget) == selected_id:
                return idx
        raise ValueError('{self!r}: Invalid current selection: {selected_id!r}')

    def selection_set(self, idx: str):
        '''Select a tab by identifier.'''
        wtab = self.wtabs.get(idx, None)
        assert wtab is not None, f'Invalid Selection: {idx}'
        return self.select(tab_id=str(wtab.widget))

    def _tabScrollUp(self, event=None):
        keys = list(self.wtabs.keys())
        selected = self.wselection()
        if selected == keys[0]:
            # First Tab
            if self.tWraparound:
                new_selected = keys[-1]
            else:
                new_selected = None
        else:
            # TODO: Optimise this? See `wselection`
            selected_idx = keys.index(selected)
            new_selected = keys[selected_idx - 1]
        if new_selected:
            self.selection_set(new_selected)

    def _tabScrollDown(self, event=None):
        keys = list(self.wtabs.keys())
        selected = self.wselection()
        if selected == keys[-1]:
            # Last Tab
            if self.tWraparound:
                new_selected = keys[0]
            else:
                new_selected = None
        else:
            # TODO: Optimise this? See `wselection`
            selected_idx = keys.index(selected)
            new_selected = keys[selected_idx + 1]
        if new_selected:
            self.selection_set(new_selected)


class NotebookUniform(Notebook):
    '''A tabbed interface to hold a series of uniform containers.

    This is a variant of the regular `Notebook` specially created to simplify
    the usual case where all the tabs are very similar (usually, they are the
    same underlying class).

    Args:
        tabids: A mapping of tab identifiers and tab titles.

    See Also:
        `Notebook`: A fully generic version of this. Don't try to make the
        `setup_tab` function too complex, move to this widget instead.
    '''
    tabids: typing.Optional[typing.Mapping[str, str]] = None

    def __init__(self, *args, tabids: typing.Optional[typing.Mapping[str, str]] = None, **kwargs):
        self.tabids = self.tabids or tabids
        if self.tabids is None:
            raise ValueError('{self!r}: Missing required tabids')
        super().__init__(*args, **kwargs)

    def setup_tabs(self, *args, **kwargs) -> typing.Mapping[str, model.NotebookTab]:
        '''Define the sub tabs, based on the common tab.

        Do not overwrite this unless you know what you are doing.

        To edit the common tab, see `setup_tab`.
        '''
        assert self.tabids is not None
        tabs = {}
        for tid, tname in self.tabids.items():
            tabs[tid] = Notebook.Tab(tname,
                                     self.setup_tab(tid, tname),
                                     *args, **kwargs)
        return tabs

    def setup_tab(self, identifier: str, name: str) -> mixin.ContainerWidget:
        '''Define the common tab `ContainerWidget` here.

        Similar to `setup_tabs <Notebook.setup_tabs>`, but for a single tab widget.
        '''
        raise NotImplementedError


class Tree(ttk.Treeview, mixin.SingleWidget):
    '''A hierarchical multicolumn data display widget.

    This widget is capable of showing a hierarchy of data records (one per
    row). Each record can have multiple columns of data.
    Each record can store arbitrary data on its `Element <model.TreeElement>`,
    exposed on the `onSelect` function.

    See `Python ttk.Treeview <tkinter.ttk.Treeview>` and ``Tk``
    `ttk.Treeview <https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm>`_
    documentation.

    Args:
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.
        label: The heading text for the first column, which includes the labels.
        columns: Mapping between column identifiers and its titles. Supports
            also a direct map between identifier and `model.TreeColumn`.
        selectable: Should the user be able to select one of the values?
            Defaults to `False`.
        openlevel: The hierarchy level to open the elements. Defaults to ``1``,
            only the toplevel elements are opened.
            Set to ``0`` to close all, and to a really big number to open all.
        expand: Grow the widget to match the container grid size. This is
            usually supported for containers, but it is included here.
        style: Configure the widget style.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `Listbox`: Simplified version of this
    '''
    Element = model.TreeElement  # Alias the tree element information  # TODO: Move TreeElement class here?

    @dataclass
    class Style(model.WStyle):
        '''`Tree` style object.

        These are the style configurations:

        Args:
            show_headings: Show column title headings.
            show_labels: Show the first column, which includes the labels.
            altbg: Show alternate backgrounds for each record.
            altbg_sindex: ``altbg`` initial alternate colour index.

        These are the colours:

        Args:
            colour_altbg: ``altbg`` alternate line colour.
                Used as the background colour.
        '''
        show_headings: bool = True
        show_labels: bool = True
        altbg: bool = True
        altbg_sindex: typing.Literal[0, 1] = 1
        # Colours
        colour_altbg: str = 'lightgrey'

    state_type = varTree
    __lines_alt: str = '__:lines-alt'

    wcolumns: typing.Mapping[str, model.TreeColumn]
    wdata: typing.MutableMapping[str, typing.Any]

    def __init__(self, parent, *, variable: typing.Optional[varTree] = None,
                 label: typing.Optional[str],
                 columns: typing.Mapping[str, typing.Union[model.TreeColumn, str]],
                 selectable: bool = False,
                 openlevel: int = 1,
                 expand: bool = True,
                 style: Style = Style(_default=True),
                 **kwargs):
        self.wstyle = style
        # TODO: Support:
        # - Setup widget column settings? See Listbox
        wcolumns = {}
        for cid, cobj in columns.items():
            if isinstance(cobj, model.TreeColumn):
                ccol = cobj
            elif isinstance(cobj, str):
                ccol = model.TreeColumn(cid, name=cobj)
            else:
                raise ValueError(f'{self!r}: Invalid column "{cid}": {cobj!r}')
            wcolumns[cid] = ccol
        self.wcolumns = wcolumns
        wshow = []
        if self.wstyle.show_headings:
            wshow.append('headings')
        if self.wstyle.show_labels:
            wshow.append('tree')
        # Initialise Variable and Data
        self.init_single(variable)
        kwargs.update({
            'show': wshow,  # Override the given `show` argument
            'selectmode': tk.BROWSE if selectable else tk.NONE,
            'columns': list(self.wcolumns.keys()),
        })
        super().__init__(parent, **kwargs)
        self.wdata = {}
        # Selection
        if selectable:
            self.binding('<Double-Button-1>', lambda e: 'break')  # Disable double click
            self.binding('<<TreeviewSelect>>', self._onSelect)
        # Appearance
        if expand:
            self.grid(sticky=tk.NSEW)
        self.openlevel: int = openlevel  # TODO: Support opening all levels, explicit?
        # # Headers
        if label is not None:
            self.heading('#0', text=label)
        for wcol in self.wcolumns.values():
            self.heading(wcol.identifier, text=wcol.name)
        # # Alternate Backgrounds
        if self.wstyle.altbg:
            self.tag_configure(Tree.__lines_alt, background=self.wstyle.colour_altbg)
            # Minor issue: There is a nearly impercetible flash of badness with
            # `TimeoutIdle` that doesn't happen when calling the function
            # directly.
            # Possible fix: in `__tree_lsvisible`, pass an optional
            # `self.focus()` ID (when != '') and open/close state, that
            # replaces `wopen`.
            altbg = self.tidle(self.__tree_altbg, key='altbg')
            self.binding('<<TreeviewOpen>>', altbg.reschedule)
            self.binding('<<TreeviewClose>>', altbg.reschedule)
        # Trace variable state
        self.trace(self.__tree_set, trace_name=f'__:{__name__}')

    def _tree_get(self, variable: var.Variable) -> typing.Sequence[model.TreeElement]:
        '''Generate a `varTree` object, based on the variable.

        Should be reimplemented by subclasses that change the variable type.
        '''
        return variable.get()

    def __tree_ls(self, parent: typing.Optional[str] = None) -> typing.Iterable[mixin.MixinWidget]:
        '''Generate a list all widget ids, in linear order.'''
        for wtop in self.get_children(item=parent):
            yield wtop
            yield from self.__tree_ls(parent=wtop)

    def __tree_lsvisible(self, parent: typing.Optional[str] = None, _kids=None) -> typing.Iterable[mixin.MixinWidget]:
        '''Generate a list of all visible widget ids, in GUI order.

        This guarantees the yielded values are visible to the user, as long as
        the tree is stable.

        See Also:
            `__tree_ls`: Show all widgets, even the not currently shown.

        Note:
            When called directly from the ``<<TreeviewOpen>>`` or
            ``<<TreeviewClose>>`` event, this will "fail", that event runs too
            early. Use a `model.TimeoutIdle` in there to get the correct
            results.
        '''
        for wtop in _kids or self.get_children(item=parent):
            yield wtop
            wopen = self.item(wtop, option='open') == 1
            wkids = self.get_children(item=wtop)
            if len(wkids) > 0 and wopen:
                yield from self.__tree_lsvisible(parent=wtop, _kids=wkids)

    def __tree_clean(self, parent=None) -> None:
        self.delete(*self.__tree_ls(parent=parent))
        self.wdata.clear()

    def __tree_put(self, elements: typing.Sequence[model.TreeElement], *,
                   parent: typing.Optional[str] = None,
                   openlevel: typing.Optional[int] = None, _level: int = 0):
        parent_loc = tk.END if parent is None else self.index(parent)
        openlevel = openlevel or self.openlevel
        for eid, element in enumerate(elements):
            # if __debug__:
            #     tpl_text = f'{parent or "__top__"}::#{eid}'
            #     logger.debug(f'{">" * (_level + 1)} {tpl_text}: L:"{element.label}" C:|{" ".join(element.columns)}|')
            if element.columns is not None:
                assert len(element.columns) == len(self.wcolumns), f'Invalid Column #{eid}: Size: E{len(element.columns)} W{len(self.wcolumns)}'
            cid = self.insert(parent or '', parent_loc,
                              text=element.label, values=element.columns or [],
                              open=_level < openlevel,
                              )
            self.wdata[cid] = element.data
            # if __debug__:
            #     logger.debug(f'{"|" * (_level + 1)} ID: {cid}')
            if element.children:
                # if __debug__:
                #     logger.debug(f'{"|" * (_level + 1)} Children: {len(element.children)}')
                self.__tree_put(element.children,
                                parent=cid,
                                openlevel=openlevel, _level=_level + 1)

    def __tree_set(self, *args, **kwargs) -> None:
        assert self.variable is not None, f'{self!r}: Missing variable'
        value = self._tree_get(self.variable)
        self.__tree_clean()
        self.__tree_put(value)
        if self.wstyle.altbg:
            self._tidles['altbg'].schedule()
        self._tree_onset(value)

    def __tree_altbg(self, *, remove: bool = False) -> None:
        '''Setup the alternate background, based on tags.

        Args:
            remove: Force removing all the backgrounds
        '''
        tname = Tree.__lines_alt
        index: int = self.wstyle.altbg_sindex
        for rid in self.__tree_lsvisible():
            tags = set(self.item(rid, option='tags'))
            dotags = False
            if not remove and index % 2 == 0:
                if tname not in tags:
                    tags.add(tname)
                    dotags = True
            else:
                if tname in tags:
                    tags.remove(tname)
                    dotags = True
            if dotags:
                self.item(rid, tags=list(tags))
            index += 1
        # if __debug__:
        #     # This should run only once, even with multiple changes
        #     if index > self.wstyle.altbg_sindex:
        #         logger.debug(f'{self}: Calculated AltBG')

    def wsid(self) -> typing.Optional[str]:
        '''Get the selected element identifier.

        Returns:
            `Element <model.TreeElement>` id, or `None` when nothing is selected.

            If the widget was created without the ``selectable`` flag, this always
            returns `None`.
        '''
        selection = self.selection()
        if __debug__:
            selectmode = str(self['selectmode'])
            assert selectmode in [tk.BROWSE, tk.NONE], f'{self!r}: Invalid Selection Mode: {selectmode}'
            logger.debug('Selection: %r', self.selection())
        if len(selection) == 0:
            # Skip un-selections
            # Usually the Tree contents changed...
            return None
        else:
            # Regular Selection
            assert len(selection) == 1, f'{self!r}: Invalid selection mode'
            treeid = selection[0]
            return treeid

    def wselection(self) -> typing.Optional[typing.Any]:
        '''Get the selected data.

        Returns:
            Since this supports only a single selection, return the selected
            value, or ``None`` when nothing is selected.

            If the widget was created without the ``selectable`` flag, this always
            returns `None`.
        '''
        wsid = self.wsid()
        return self.wdata[wsid] if wsid else None

    def _onSelect(self, event=None):
        ''''''  # Internal, do not document
        selection: tuple = self.selection()
        if __debug__:
            selectmode = str(self['selectmode'])
            assert selectmode in [tk.BROWSE, tk.NONE], f'{self!r}: Invalid Selection Mode: {selectmode}'
            # logger.debug('Selection: %r', self.selection())
        if len(selection) == 0:
            # Skip
            # - NONE selectmode
            # - un-selections (usually the Tree contents changed)
            pass
        else:
            # Regular Selection
            assert len(selection) == 1, f'{self!r}: Invalid selection mode'
            treeid = selection[0]
            data = self.wdata[treeid]
            self.onSelect(treeid, data)

    def _tree_onset(self, value: typing.Sequence[model.TreeElement]) -> None:
        '''Callback to be executed when setting a different value.

        Available for subclass redefinition.
        '''
        pass

    def onSelect(self, treeid: str, data: typing.Any = None) -> None:
        '''Callback to be executed when clicking this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.

        Args:
            treeid: The selected tree id
            data: The arbitrary data associated with the element. Defaults to `None`.
        '''
        pass


class Listbox(Tree):
    '''A listbox widget, a list of strings.

    This is a modern variation of the listbox, a way to display several rows of
    content (simple strings, in this case), and be able to select one at a
    time.

    The ``height`` can be hardcoded to a value, or it can vary with the
    contents. Note that the ``maxHeight`` is smaller than the amount of rows to
    display, no scrollbar is shown, but the list can be
    scrolled with the mouse wheel.
    The automatic variation on the height size (AKA auto-height) can be
    completely disabled by setting all height-related arguments to `None`. This
    is the default. The ``expand`` argument is set to `False` when the
    auto-height is disabled.

    Each string is centered on the list. This can be tweaked using the
    ``columnConfig`` argument.

    The state is a `list` of `str` values, `var.StringList`.

    This is a variation on the `Tree` widget, with a single column, a different
    variable type and some overriden default values.
    See also `Python ttk.Treeview <tkinter.ttk.Treeview>` and ``Tk``
    `ttk.Treeview <https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm>`_
    documentation.

    Args:
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.
        label: The label to include besides the listbox. Can be given as a
            class variable.
            Optional, when given is show as the single column heading.
        columnConfig: Override configuration for the single column. Advanced
            usage only.
        height: If given, always show this quantity of rows.
            If it is `None`, the number of permanently shown rows will vary between
            ``minHeight`` and ``maxHeight``.
        minHeight: If ``height`` is `None`, make sure this number of rows is
            always visible.
            Optional, when `None`, there's no lower limit on the visible number
            of rows.
        maxHeight: If ``height`` is `None`, make sure there are no more
            visible rows than this number.
            Optional, when `None`, there's no upper limit on the visible
            number of rows.
        selectable: See `Tree` for its meaning.
            Defaults to `True`.
        style_altbg: See `Tree` for its meaning.
            Defaults to `False`.
        expand: See `Tree` for its meaning.
            Defaults to `False`, but interacts with the auto-height settings.
        style: Configure the widget style.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
    '''
    label: typing.Optional[str] = None

    @dataclass
    class Style(Tree.Style):
        '''`Listbox` style object.

        See `Tree.Style` for upstream values, these are the differences:

        Args:
            altbg: Disabled by default.
            show_labels: Unsupported.
        '''
        altbg: bool = False
        show_labels: bool = False

        if __debug__:
            def __post_init__(self):
                if self.show_labels:
                    warnings.warn(f'{self}: Unsupported "show_labels"', stacklevel=3)
                self.show_labels = False

    state_type = var.StringList  # type: ignore  # Change the variable type

    def __init__(self, *args, variable: typing.Optional[var.StringList] = None,
                 label: typing.Optional[str] = None,
                 columnConfig: typing.Mapping[str, typing.Any] = None,
                 height: typing.Optional[int] = None, minHeight: typing.Optional[int] = None, maxHeight: typing.Optional[int] = None,
                 selectable: bool = True, expand: typing.Optional[bool] = None,  # Override
                 style: Style = Style(_default=True),
                 **kwargs):
        chosen_label = self.label or label
        if style._default:
            style.show_headings = chosen_label is not None
        kwargs.update({
            'label': chosen_label,
            'variable': variable,
            'selectable': selectable,  # Override
            'columns': {'label': chosen_label or 'Label'},  # Single Column "label"
            'style': style,
        })
        # Configure height
        self.heightRange: typing.Optional[typing.Tuple[typing.Optional[int], typing.Optional[int]]]
        if height is None:
            self.heightRange = minHeight, maxHeight
        else:
            kwargs['height'] = height  # Hardcode the height value
            self.heightRange = None
        if height or minHeight or maxHeight and expand is None:
            # Don't expand when the fixed or varying height is set
            expand = False
        # Configure (single) column
        # - Don't use `#0` since that is not properly centered, it has the tree
        #   elements in there, even hidden.
        cConfig = {
            'anchor': tk.CENTER,
            'stretch': True,
        }
        if columnConfig:
            cConfig.update(columnConfig)
        if expand is not None:
            kwargs['expand'] = expand
        super().__init__(*args, **kwargs)
        self.column('label', **cConfig)

    def _tree_get(self, variable: var.Variable) -> typing.Sequence[model.TreeElement]:
        return [model.TreeElement(label=e, columns=[e], data=e) for e in variable.get()]

    def _tree_onset(self, value: typing.Sequence[model.TreeElement]) -> None:
        if self.heightRange is not None:
            minHeight, maxHeight = self.heightRange
            wsize = None
            if minHeight:
                wsize = max(minHeight, len(value))
            if maxHeight:
                wsize = min(maxHeight, wsize or len(value))
            if wsize:
                if __debug__:
                    logger.debug(f'{self}: Auto Height: {wsize}')
                self.configure(height=wsize)
