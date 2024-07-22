
# sim928_ophyd.py


from ophyd import Device, Component as Cpt
from instrument_base import BasicSignal
from sim928 import SIM928

class SIM928Controller(Device):
    voltage = Cpt(BasicSignal, get_func=None, set_func=None)

    def __init__(self, name, visa_address, slot, **kwargs):
        super().__init__(name=name, **kwargs)
        self.sim928 = SIM928(visa_address)
        self.slot = slot
        self.voltage.get_func = self._get_voltage
        self.voltage.set_func = self._set_voltage

    def _set_voltage(self, voltage):
        self.sim928.set_voltage(self.slot, voltage)

    def _get_voltage(self):
        return self.sim928.get_voltage(self.slot)
