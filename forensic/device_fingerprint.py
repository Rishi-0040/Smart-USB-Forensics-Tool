import wmi
import sqlite3
from datetime import datetime

DB_NAME = "usb_forensics.db"

def create_device_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usb_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            device_name TEXT,
            device_id TEXT,
            vendor_id TEXT,
            product_id TEXT,
            trusted INTEGER
        )
    """)

    conn.commit()
    conn.close()

def extract_vendor_product(device_id):

    vendor_id = "UNKNOWN"
    product_id = "UNKNOWN"
    
    try:
        parts = device_id.split("\\")
        if len(parts) > 1:
            ids = parts[1]

            for item in ids.split("&"):
                if item.startswith("VID_"):
                    vendor_id = item.replace(
                        "VID_",
                        ""
                    )
                elif item.startswith("PID_"):
                    product_id = item.replace(
                        "PID_",
                        ""
                    )
    except:
        pass
    return vendor_id, product_id

def save_device(
    device_name,
    device_id,
    vendor_id,
    product_id,
    trusted
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    cursor.execute("""
        INSERT INTO usb_devices (
            timestamp,
            device_name,
            device_id,
            vendor_id,
            product_id,
            trusted
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        device_name,
        device_id,
        vendor_id,
        product_id,
        trusted
    ))

    conn.commit()
    conn.close()

def scan_usb_devices():

    create_device_table()
    c = wmi.WMI()
    print("\n========== USB DEVICE SCAN ==========\n")

    for usb in c.Win32_USBHub():
        device_name = usb.Name
        device_id = usb.DeviceID
        vendor_id, product_id = extract_vendor_product(device_id)
        trusted = 0

        #Example trusted rule
        if "sanDisk" in device_name:
            trusted = 1

        save_device(
            device_name,
            device_id,
            vendor_id,
            product_id,
            trusted
        )

        print(f"DEVICE NAME: {device_name}")
        print(f"DEVICE ID: {device_id}")
        print(f"VENDOR ID: {vendor_id}")
        print(f"PRODUCT ID: {product_id}")

        if trusted:
            print("STATUS      : TRUSTED DEVICE ✅")

        else:

            print("STATUS      : UNKNOWN DEVICE ⚠️")
        
        print("-----------------------------------")


if __name__ == "__main__":

    scan_usb_devices()