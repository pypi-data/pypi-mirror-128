"""Docstring."""
from typing import Optional


class Baz:
    """Baz test class."""

    attr = 1


class Foo:
    """Foo test class."""

    attr: str = 'test'

    def meth(self) -> Baz:
        """Test method."""


def bar() -> Foo:
    """bar test function."""


def optional() -> Optional[Foo]:
    """Return optional type."""


def compile():
    """Shadows built in compile function."""
