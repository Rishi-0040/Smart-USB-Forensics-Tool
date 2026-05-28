from database.db_manager import create_tables, connect_db


def fetch_device_history():
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            device_name,
            vendor_id,
            product_id,
            trusted
        FROM usb_devices
        ORDER BY timestamp DESC
""")
    
    devices = cursor.fetchall()
    conn.close()
    return devices