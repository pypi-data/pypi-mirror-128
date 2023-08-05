import typing

from pyobs.utils.threads import Future
from pyobs.utils.enums import ExposureStatus
from .IAbortableProxy import IAbortableProxy
from .interfaceproxy import InterfaceProxy


class ISpectrographProxy(IAbortableProxy, InterfaceProxy):
    def abort(self) -> Future[None]:
        ...

    def get_exposure_progress(self) -> Future[float]:
        ...

    def get_exposure_status(self) -> Future[ExposureStatus]:
        ...

    def grab_spectrum(self, broadcast: bool = True) -> Future[str]:
        ...

