__version__ = "2.1.0"
__version_info__ = tuple(
    map(
        lambda val: int(val) if val.isnumeric() else val,
        __version__.split("."),
    )
)

from . import ensure_context, exc
from ._datastructures import ImmutableAsyncProvider, ImmutableSyncProvider, StateWrapper
from .context import AsyncContext, SyncContext
from .generic import AsyncGenericFactory, GenericFactory
from .getters import ArgType, context_factory, get_context

__all__ = [
    "AsyncContext",
    "SyncContext",
    "context_factory",
    "get_context",
    "GenericFactory",
    "AsyncGenericFactory",
    "exc",
    "ensure_context",
    "ArgType",
    "ImmutableSyncProvider",
    "ImmutableAsyncProvider",
    "StateWrapper",
]
