from itertools import tee
import os
from datetime import datetime
from pathlib import Path
from bluesky import RunEngine
from bluesky.plans import list_scan
from bluesky.utils import PersistentDict
from databroker.v2 import temp
from sim928_ophyd import SIM928Controller
from SR830_ophyd import SR830Device
import pandas as pd

RE = RunEngine()

# Persistent metadata storage
metadata_path = Path("~/.bluesky_history").expanduser()
RE.md = PersistentDict(metadata_path)

# Temporary catalog setup
catalog = temp()
RE.subscribe(catalog.v1.insert)

# Connect to devices
sr830_device = SR830Device(address='TCPIP0::192.168.0.10::1234::SOCKET', gpib_address=9, name='sr830')
sim928_device = SIM928Controller(name='sim928', visa_address="TCPIP0::ir-moxa01.psi.ch::3002::SOCKET", slot=2)

sr830_device.wait_for_connection()
sim928_device.wait_for_connection()

# Function to print readings from events
def print_readings(name, doc):
    if name == 'event':
        data = doc['data']
        freq = data.get('sr830_freq', 'N/A')
        voltage = data.get('sim928_voltage', 'N/A')
        print(f"Frequency: {freq} Hz, Voltage: {voltage} V")

RE.subscribe(print_readings)

# Function to create a unique file prefix
def create_unique_file_prefix(prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"

# Function to export documents to CSV
def export(docs, directory, file_prefix):
    if not os.path.exists(directory):
        os.makedirs(directory)

    unique_file_prefix = create_unique_file_prefix(file_prefix)
    csv_file_path = os.path.join(directory, f"{unique_file_prefix}_primary.csv")

    # Convert generator to list
    docs_list = list(docs)

    # Extract data for CSV export
    data = []
    for name, doc in docs_list:
        if name == 'event_page':
            event_data = doc['data']
            data.append({
                'Time': doc['time'][0],
                'SR830 Frequency': event_data['sr830_freq'][0],
                'SIM928 Voltage': event_data['sim928_voltage'][0],
                'Sequence Number': doc['seq_num'][0]
            })

    # Create a DataFrame and export to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)

    print(f"Exported data to {csv_file_path}")
    return csv_file_path

# Function to display the CSV data in a pretty format
def display_csv(csv_file):
    df = pd.read_csv(csv_file)
    print(df.to_string(index=False))

# Run the scan
RE(list_scan([sr830_device, sim928_device], sim928_device.voltage, [1, 2, 3, 4, 5]))

# Export the data after the scan
docs = catalog[-1].documents(fill="no")

output_directory = os.path.join(os.getcwd(), "experiment_data")
file_prefix = 'sample_scan'

# Ensure to handle potential issues with export
try:
    csv_file = export(docs, output_directory, file_prefix)
    display_csv(csv_file)
except Exception as e:
    print(f"An error occurred during export: {e}")
