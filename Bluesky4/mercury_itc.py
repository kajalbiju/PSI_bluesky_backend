# mercury_itc.py
import pyvisa
from instrument_base import InstrumentBase


device_address = "STILL_DB6.T1"

class MercuryITC(InstrumentBase):
    def connect(self):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(self.address)
        self.instrument.timeout = 10000
        self.instrument.write_termination = '\n'
        self.instrument.read_termination = '\n'

    def disconnect(self):
        if self.instrument:
            self.instrument.close()

    def query(self, command):
        try:
            self.connect()
            response = self.instrument.query(command)
            return response
        except pyvisa.errors.VisaIOError as e:
            print(f"Error during query: {e}")
            return None
        finally:
            self.disconnect()

    def write(self, command):
        try:
            self.connect()
            self.instrument.write(command)
        except pyvisa.errors.VisaIOError as e:
            print(f"Error during write: {e}")
        finally:
            self.disconnect()

    
    def read_temperature(self):
        command = f"READ:DEV:{device_address}:TEMP:SIG:TEMP"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                # Extract the numeric part of the response and convert to float
                temperature_str = response.split(":")[-1].strip().rstrip("K")
                temperature = float(temperature_str)
                return temperature
            except ValueError:
                print(f"Invalid temperature format: {response}")
        else:
            print("Temperature reading is not available.")
        return None

    def set_gas_flow(self, temperature):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:TSET:{temperature}"
        self.write(command)
        response = self.query("READ:DEV:{device_address}:TEMP:SIG:TEMP")
        return response

    def set_p_value(self, p_value):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:P:{p_value}"
        self.write(command)
        response = self.query(f"READ:DEV:{device_address}:TEMP:LOOP:P")
        return response

    def set_i_value(self, i_value):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:I:{i_value}"
        self.write(command)
        response = self.query(f"READ:DEV:{device_address}:TEMP:LOOP:I")
        return response

    def set_d_value(self, d_value):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:D:{d_value}"
        self.write(command)
        response = self.query(f"READ:DEV:{device_address}:TEMP:LOOP:D")
        return response

    def set_heater_setpoint(self, h_setpoint):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:HSET:{h_setpoint}"
        self.write(command)
        response = self.query(f"READ:DEV:{device_address}:TEMP:LOOP:HSET")
        return response

    def set_flow_setpoint(self, f_setpoint):
        command = f"SET:DEV:{device_address}:TEMP:LOOP:FSET:{f_setpoint}"
        self.write(command)
        response = self.query(f"READ:DEV:{device_address}:TEMP:LOOP:FSET")
        return response

    def get_gas_flow(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:TSET"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                return float(response.split(':')[-1])
            except ValueError:
                print(f"Invalid format for gas flow: {response}")
        else:
            print("Gas flow reading is not available.")
        return None

    def get_p_value(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:P"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                return float(response.split(':')[-1])
            except ValueError:
                print(f"Invalid format for P value: {response}")
        else:
            print("P value reading is not available.")
        return None

    def get_i_value(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:I"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                return float(response.split(':')[-1])
            except ValueError:
                print(f"Invalid format for I value: {response}")
        else:
            print("I value reading is not available.")
        return None

    def get_d_value(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:D"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                return float(response.split(':')[-1])
            except ValueError:
                print(f"Invalid format for D value: {response}")
        else:
            print("D value reading is not available.")
        return None

    def get_heater_setpoint(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:HSET"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                return float(response.split(':')[-1])
            except ValueError:
                print(f"Invalid format for heater setpoint: {response}")
        else:
            print("Heater setpoint reading is not available.")
        return None


    def get_gas_flow(self):
        command = f"READ:DEV:{device_address}:TEMP:LOOP:TSET"
        response = self.query(command)
        if response and 'N/A' not in response:
            try:
                value_str = response.split(':')[-1]  # Extract the value part
                value_str = value_str.strip()  # Remove any leading/trailing whitespace
                value = float(value_str[:-1])  # Convert to float, excluding the last character ('K')
                return value
            except ValueError:
                print(f"Invalid format for gas flow: {response}")
        else:
            print("Gas flow reading is not available.")
        return None