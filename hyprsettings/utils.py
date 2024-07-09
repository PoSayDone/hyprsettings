from gi.repository import GObject
from typing import Optional


def GProperty(
    type: type,
    default: Optional[object] = None,
    *args,
    readable: bool = True,
    writable: bool = True,
    construct: bool = False,
    construct_only: bool = False,
    additional_flags: GObject.ParamFlags = GObject.ParamFlags(0),
    **kwargs,
) -> GObject.Property:
    """A wrapper around GObject.Property decorator

    Provides shorter syntax for creating GObject properties.
    """

    flags = additional_flags
    if readable:
        flags |= GObject.ParamFlags.READABLE
    if writable:
        flags |= GObject.ParamFlags.WRITABLE
    if construct:
        flags |= GObject.ParamFlags.CONSTRUCT
    if construct_only:
        flags |= GObject.ParamFlags.CONSTRUCT_ONLY

    return GObject.Property(*args, type=type, default=default, flags=flags, **kwargs)
