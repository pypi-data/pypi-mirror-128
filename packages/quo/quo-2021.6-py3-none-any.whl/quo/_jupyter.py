from typing import Any, Dict, Iterable, List

from .segment import Segment
from .terminal_theme import DEFAULT_TERMINAL_THEME


JUPYTER_HTML_FORMAT = """\
<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
"""


class JupyterRenderable:
    """A shim to write html to Jupyter notebook."""

    def __init__(self, html: str, text: str) -> None:
        self.html = html
        self.text = text

    def _repr_mimebundle_(
        self, include: Iterable[str], exclude: Iterable[str], **kwargs: Any
    ) -> Dict[str, str]:
        data = {"text/plain": self.text, "text/html": self.html}
        if include:
            data = {k: v for (k, v) in data.items() if k in include}
        if exclude:
            data = {k: v for (k, v) in data.items() if k not in exclude}
        return data
#from quo.console import Console

def _get_console() -> "Console":
    """Get a global :class:`~quo.console.Console` instance. This function is used when Quo requires a Console,
    and hasn't been explicitly given one.

    Returns:
        Console: A console instance.
    """
    from quo.console.console import Console
    global _console
    if _console is None:

        _console = Console()

    return _console

class JupyterMixin:
    """Add to an Rich renderable to make it render in Jupyter notebook."""

    __slots__ = ()

    def _repr_mimebundle_(
        self, include: Iterable[str], exclude: Iterable[str], **kwargs: Any
    ) -> Dict[str, str]:
        console = _get_console()
        segments = list(console.render(self, console.options))  # type: ignore
        html = _render_segments(segments)
        text = console._render_buffer(segments)
        data = {"text/plain": text, "text/html": html}
        if include:
            data = {k: v for (k, v) in data.items() if k in include}
        if exclude:
            data = {k: v for (k, v) in data.items() if k not in exclude}
        return data


def _render_segments(segments: Iterable[Segment]) -> str:
    def escape(text: str) -> str:
        """Escape html."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    fragments: List[str] = []
    append_fragment = fragments.append
    theme = DEFAULT_TERMINAL_THEME
    for text, style, control in Segment.simplify(segments):
        if control:
            continue
        text = escape(text)
        if style:
            rule = style.get_html_style(theme)
            text = f'<span style="{rule}">{text}</span>' if rule else text
            if style.link:
                text = f'<a href="{style.link}">{text}</a>'
        append_fragment(text)

    code = "".join(fragments)
    html = JUPYTER_HTML_FORMAT.format(code=code)

    return html


def display(segments: Iterable[Segment], text: str) -> None:
    """Render segments to Jupyter."""
    from IPython.display import display as ipython_display

    html = _render_segments(segments)
    jupyter_renderable = JupyterRenderable(html, text)
    ipython_display(jupyter_renderable)


def echo(*args: Any, **kwargs: Any) -> None:
    """Proxy for Console print."""
    console = _get_console()
    return console.echo(*args, **kwargs)
