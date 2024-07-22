# SR830.py


#TCPIP0::Prologix-00-21-69-01-3f-33.psi.ch::1234::SOCKET

import pyvisa
import time

class SR830:
    def __init__(self, address, gpib_address, timeout=10000):
        self.rm = pyvisa.ResourceManager()
        self.address = address
        self.gpib_address = gpib_address
        self.timeout = timeout
        self.instrument = None

    def connect(self):
        self.instrument = self.rm.open_resource(self.address, timeout=self.timeout)
        self.instrument.write_termination = '\n'
        self.instrument.read_termination = '\n'

    def disconnect(self):
        if self.instrument:
            self.instrument.close()
            self.instrument = None

    def set_gpib_address(self):
        print(f"Setting GPIB address to {self.gpib_address}")
        self.instrument.write(f"++addr {self.gpib_address}")
        time.sleep(0.5)  # Delay to ensure command is processed

    def query(self, command):
        self.set_gpib_address()
        print(f"Sending command: {command.strip()}")
        self.instrument.write(command)
        time.sleep(0.5)  # Delay to ensure command is processed
        response = self.instrument.read()
        return response

    def get_idn(self):
        return self.query("*IDN?")

    def get_param(self, param):
        return self.query(param)

    def close(self):
        self.disconnect()

if __name__ == "__main__":
    # Example usage
    address = 'TCPIP0::Prologix-00-21-69-01-3f-33.psi.ch::1234::SOCKET'  # Update this with your Prologix IP address and port
    gpib_address = 9  # Set your GPIB address

    sr830 = SR830(address, gpib_address)
    try:
        sr830.connect()
        idn = sr830.get_idn()
        print(f"IDN: {idn}")

        # Example: Get frequency
        freq = sr830.get_param("FREQ?")
        print(f"Frequency: {freq}")
    except pyvisa.errors.VisaIOError as e:
        print(f"An error occurred: {e}")
    finally:
        sr830.close()


