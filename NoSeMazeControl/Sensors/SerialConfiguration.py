import serial
import serial.tools.list_ports as s_ports
import time
import sys    
from Sensors import constants

def configure_serial():
    """Method to send ID commands to sensors connected to COM ports
    Sensornodes store their respective IDs in non-volatile memory
    """
    constants.SNIds = []

    # Iterate over ID\COM pairs and send a serial command to the port
    for sensor_id, com_port in constants.sensor_com_pairs:
        
        if sensor_id == "gravity":
            try:
                ser = serial.Serial(f"COM{com_port}", 115200, timeout = 0.5)
                constants.gravity_port = com_port
            except:
                print(f"COM Port {com_port} not open")
        else:
            # This command sets the ID in the nodes NVS memory
            send_buf = f"SetID 0x{sensor_id}\n"
            try:
                ser = serial.Serial(f"COM{com_port}", 115200, timeout = 0.5)
                ser.reset_input_buffer()
                ser.write(send_buf.encode())
                response = ser.readline().decode()
                
                if response == "ESP-ROM:esp32s2-rc4-20191025":
                    print("Repeating")
                    ser.reset_input_buffer()
                    ser.write(send_buf.encode())
                else:
                    print("Opened without repeating")
                ser.flush()
                constants.SNIds.append(int(sensor_id))
                
            except:
                print(f"COM Port {com_port} not open")
