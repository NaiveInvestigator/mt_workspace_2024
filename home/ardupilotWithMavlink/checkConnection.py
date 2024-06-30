from pymavlink import mavutil
import time 

# Replace '/dev/ttyACM0' with your port (e.g., 'COM3' on Windows)
connection_string = '/dev/ttyACM2'
baud_rate = 115200

# Create the connection
master = mavutil.mavlink_connection(connection_string, baud=baud_rate)

# Wait for the first heartbeat to find the system ID
print("Waiting for heartbeat...")
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

# Fetch and print data continuously
while True:
    try:
        msg = master.recv_match(blocking=True)
        if not msg:
            continue

        if msg.get_type() == 'ATTITUDE':
            print(f"Pitch: {msg.pitch}, Roll: {msg.roll}, Yaw: {msg.yaw}")
        time.sleep(.1)

    except KeyboardInterrupt:
        print("Exiting...")
        break

