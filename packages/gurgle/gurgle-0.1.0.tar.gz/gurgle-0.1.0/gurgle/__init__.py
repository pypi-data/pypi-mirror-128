"""Wrappers to extend ML processing components (perform online/mini-batch learning,
track residues, store data, track drift etc.)"""

from gurgle.base import (
    enable_incremental_learning_on_call,
    CallableModel,
    identity_func,
    TransparentModel,
)
