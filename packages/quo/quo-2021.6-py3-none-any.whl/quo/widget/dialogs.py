"""
Collection of reusable components for building full screen applications.
"""
from typing import (
        Optional,
        Sequence,
        Union
        )

from quo.filters import has_completions, has_focus
from quo.text import Textual
from quo.keys.key_binding.bindings.focus import focus_next, focus_previous
from quo.keys import KeyBinder
from quo.layout.containers import (
    AnyContainer,
    DynamicContainer,
    HSplit,
    VSplit,
)
from quo.layout.dimension import AnyDimension
from quo.layout.dimension import Dimension as D

from .core import (
        Box,
        Button, 
        Frame,
        Shadow
        )

__all__ = [
        "Dialog",
        ]


class Dialog:
    """
    Simple dialog window. This is the base for input dialogs, message dialogs
    and confirmation dialogs.

    Changing the title and body of the dialog is possible at runtime by
    assigning to the `body` and `title` attributes of this class.

    :param body: Child container object.
    :param title: Text to be displayed in the heading of the dialog.
    :param buttons: A list of `Button` widgets, displayed at the bottom.
    """

    def __init__(
        self,
        body: AnyContainer,
        title: Textual = "",
        buttons: Optional[Sequence[Button]] = None,
        modal: bool = True,
        width: AnyDimension = None,
        background: bool = False,
    ) -> None:

        self.body = body
        self.title = title

        buttons = buttons or []

        # When a button is selected, handle left/right key bindings.
        b_kb = KeyBinder()
        if len(buttons) > 1:
            first_selected = has_focus(buttons[0])
            last_selected = has_focus(buttons[-1])

            b_kb.add("left", filter=~first_selected)(focus_previous)
            b_kb.add("right", filter=~last_selected)(focus_next)

        frame_body: AnyContainer
        if buttons:
            frame_body = HSplit(
                [
                    # Add optional padding around the body.
                    Box(
                        body=DynamicContainer(lambda: self.body),
                        padding=D(preferred=1, max=1),
                        padding_bottom=0,
                    ),
                    # The buttons.
                    Box(
                        body=VSplit(buttons, padding=1, key_bindings=b_kb),
                        height=D(min=1, max=3, preferred=3),
                    ),
                ]
            )
        else:
            frame_body = body

        # Key bindings for whole dialog.
        kb = KeyBinder()
        kb.add("tab", filter=~has_completions)(focus_next)
        kb.add("s-tab", filter=~has_completions)(focus_previous)

        frame = Shadow(
            body=Frame(
                title=lambda: self.title,
                body=frame_body,
                style="class:dialog.body",
                width=(None if background is None else width),
                key_bindings=kb,
                modal=modal,
            )
        )

        self.container: Union[Box, Shadow]
        if background:
            self.container = Box(
                    body=frame,
                    style="class:dialog",
                    width=width
                    )
        else:
            self.container = frame

    def __pt_container__(self) -> AnyContainer:
        return self.container
