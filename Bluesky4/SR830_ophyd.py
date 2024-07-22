from ophyd import Device, Component as Cpt, Signal
import pyvisa
from SR830 import SR830

class SR830Device(Device):
    idn = Cpt(Signal, value="")
    freq = Cpt(Signal, value=0.0)

    def __init__(self, address, gpib_address, name="sr830", **kwargs):
        super().__init__(name=name, **kwargs)
        self.sr830 = SR830(address, gpib_address)

    def connect(self):
        self.sr830.connect()

    def disconnect(self):
        self.sr830.disconnect()

    def read_idn(self):
        idn = self.sr830.get_idn()
        self.idn.put(idn)
        return idn

    def read_frequency(self):
        freq = self.sr830.get_param("FREQ?")
        self.freq.put(float(freq))
        return freq

    def close(self):
        self.sr830.close()

# Example usage
if __name__ == "__main__":
    address = 'TCPIP0::Prologix-00-21-69-01-3f-33.psi.ch::1234::SOCKET'  # Update this with your Prologix IP address and port
    gpib_address = 9  # Set your GPIB address

    sr830_device = SR830Device(address, gpib_address, name="sr830")
    try:
        sr830_device.connect()
        idn = sr830_device.read_idn()
        print(f"IDN: {idn}")

        freq = sr830_device.read_frequency()
        print(f"Frequency: {freq}")
    except pyvisa.errors.VisaIOError as e:
        print(f"An error occurred: {e}")
    finally:
        sr830_device.close()
