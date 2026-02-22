import asyncio
from bleak import BleakScanner
import pandas as pd
import time

# Read Bluetooth mapping
devices = pd.read_csv("bluetooth_devices.csv", dtype=str)

# Time settings
CHECK_INTERVAL = 60       # check every 1 minute
MAX_OUT_TIME = 120        # demo = 2 minutes
# real system = 7200 (2 hours)

# Dictionary to track out time
out_time = {}

# Scan nearby bluetooth devices
async def scan():
    found = await BleakScanner.discover(timeout=5)
    return [d.name for d in found if d.name]

# Cancel attendance function
def cancel_attendance(roll_no):
    df = pd.read_excel("attendance_today.xlsx", dtype=str)
    df.loc[df["Roll No"] == roll_no, "Status"] = "CANCELLED"
    df.to_excel("attendance_today.xlsx", index=False)
    print("❌ Attendance CANCELLED:", roll_no)

# Continuous monitoring
while True:
    names = asyncio.run(scan())

    for _, row in devices.iterrows():
        roll_no = row["roll_no"]
        device_name = row["device_name"]

        if device_name in names:
            print(roll_no, "IN RANGE")
            out_time[roll_no] = 0
        else:
            print(roll_no, "OUT OF RANGE")
            out_time[roll_no] = out_time.get(roll_no, 0) + CHECK_INTERVAL

        if out_time[roll_no] >= MAX_OUT_TIME:
            cancel_attendance(roll_no)

    time.sleep(CHECK_INTERVAL)
