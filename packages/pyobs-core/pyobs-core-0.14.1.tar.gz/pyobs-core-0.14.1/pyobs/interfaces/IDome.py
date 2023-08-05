from .IRoof import IRoof
from .IPointingAltAz import IPointingAltAz


class IDome(IRoof, IPointingAltAz):
    """The module controls a dome, i.e. a :class:`~pyobs.interfaces.IRoof` with a rotating roof."""
    __module__ = 'pyobs.interfaces'
    pass


__all__ = ['IDome']
