import wmi
import time

c= wmi.WMI()

connected_devices= set()
while True:
    currunt_devices= set()

    for usb in c.Win32_USBHub():
        devices_id= usb.DeviceID
        currunt_devices.add(devices_id)

        if devices_id not in connected_devices:
            print(f"[+] USB Connected: {usb.Name}")
            print(f"    Device ID: {devices_id}")

    removed= connected_devices - currunt_devices

    for device in removed:
        print(f"[-] USB Removed: {device}")

    connected_devices = currunt_devices

    time.sleep(2)