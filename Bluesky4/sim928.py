# sim928.py
import pyvisa
import time
from instrument_base import InstrumentBase

class SIM928(InstrumentBase):
    def connect(self):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(self.address, timeout=10000)
        self.instrument.write_termination = '\n'
        self.instrument.read_termination = '\n'

    def disconnect(self):
        if self.instrument:
            self.instrument.close()

    #def query(self, command):
    #   try:
    #       self.connect()
    #       response = self.instrument.query(command)
    #       return response
    #   except pyvisa.errors.VisaIOError as e:
    #       print(f"Error during query: {e}")
    #       return None
    #   finally:
    #       self.disconnect()

    def query(self, command, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                self.connect()
                response = self.instrument.query(command)
                return response
            except pyvisa.errors.VisaIOError as e:
                print(f"Error during query (retry {retries + 1}): {e}")
                retries += 1
                time.sleep(1)  # Add a delay between retries if needed
            finally:
                self.disconnect()

        print(f"Failed to execute query after {max_retries} retries.")
        return None

    def write(self, command):
        try:
            self.connect()
            self.instrument.write(command)
        except pyvisa.errors.VisaIOError as e:
            print(f"Error during write: {e}")
        finally:
            self.disconnect()

    def connect_to_slot(self, slot):
        connect_command = f'CONN {slot}, "XYZZ"'
        self.write(connect_command)

    def query_idn(self):
        idn_command = '*IDN?'
        response = self.query(idn_command)
        if response:
            print(f"IDN response: {response.strip()}")
        else:
            print(f"Failed to get IDN response.")

    def set_voltage(self, slot, voltage):
       self.connect_to_slot(slot)
       command = f'VOLT {voltage}'
       self.write(command)
       self.write('XYZZ')  # Disconnect from slot

#   def get_voltage(self, slot):
#       self.connect_to_slot(slot)
#       command = 'VOLT?'
#       response = self.query(command)
#       if response:
#           return float(response.strip())
#       self.write('XYZZ')  # Disconnect from slot
#       return None


#    def set_voltage(self, slot, voltage, max_retries=3):
#        retries = 0
#        while retries < max_retries:
#            try:
#                self.connect_to_slot(slot)
#                command = f'VOLT {voltage}'
#                self.write(command)
#                # Verify that the voltage was set correctly
#                set_voltage = self.get_voltage(slot)
#                if set_voltage == voltage:
#                    print(f"Voltage set to {voltage} successfully.")
#                    self.write('XYZZ')  # Disconnect from slot
#                    return
#                else:
#                    print(f"Voltage verification failed (retry {retries + 1}).")
#            except Exception as e:
#                print(f"Error setting voltage (retry {retries + 1}): {e}")
#            finally:
#                self.write('XYZZ')  # Disconnect from slot
#                retries += 1
#                time.sleep(1)  # Add a delay between retries if needed

    def get_voltage(self, slot, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                self.connect_to_slot(slot)
                command = 'VOLT?'
                response = self.query(command)
                if response:
                    return float(response.strip())
                else:
                    print(f"Failed to get voltage (retry {retries + 1})")
                self.write('XYZZ')  # Disconnect from slot
            except Exception as e:
                print(f"Error getting voltage (retry {retries + 1}): {e}")
                retries += 1
                time.sleep(1)  # Add a delay between retries if needed
            finally:
                self.write('XYZZ')  # Disconnect from slot

        print(f"Failed to get voltage after {max_retries} retries.")
        return None



