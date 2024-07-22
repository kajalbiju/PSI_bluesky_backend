#mercury_itc_ophyd.py


from ophyd import Device, Component as Cpt
from instrument_base import BasicSignal
from mercury_itc import MercuryITC

class MercuryITCController(Device):
    temperature = Cpt(BasicSignal, get_func=None)
    d_value = Cpt(BasicSignal, get_func=None)

    def __init__(self, name, visa_address, **kwargs):
        super().__init__(name=name, **kwargs)
        self.mercury = MercuryITC(visa_address)
        self.temperature.get_func = self.mercury.read_temperature
        self.d_value.get_func = self.mercury.get_d_value


