"""Classiq SDK."""

from classiq._version import VERSION as _VERSION
from classiq.async_utils import enable_jupyter_notebook, is_notebook as _is_notebook
from classiq.authentication.authentication import (  # noqa: F401
    register_device as authenticate,
)
from classiq.client import configure  # noqa: F401

__version__ = _VERSION

if _is_notebook():
    enable_jupyter_notebook()
