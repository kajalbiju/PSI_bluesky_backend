# instrument_base.py
from abc import ABC, abstractmethod

class InstrumentBase(ABC):
    def __init__(self, address):
        self.address = address
        self.instrument = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def query(self, command):
        pass

    @abstractmethod
    def write(self, command):
        pass


#Basic Signal class

from ophyd.signal import Signal

class BasicSignal(Signal):
    def __init__(self, *args, get_func=None, set_func=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._metadata.update(
            connected=True,
            write_access=True,
        )
        self.get_func = get_func
        self.set_func = set_func

    def get(self):
        self._readback = self.get_func()
        return self._readback

    def put(self, value, *, timestamp=None, force=False):
        self._readback = value
        self.set_func(value)
