"""
This module read the rfid tag of the mouse present at the port. It differs
between Autonomouse 1 and Autonomouse 2. Both are written here. The one that
is not used should be check as commentar.
"""

import serial
import datetime

# Autonomouse 1
def check_rfid(port, n):
    """
    Parameters
    ----------
    port : str
        COM-port of rfid reader.
    
    n : int
        Total number of ID. In this case 10.
    
    Return
    ------
    out : str
        ID of mouse present.
    """
    
    ser = serial.Serial(port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=2)
    rfid = ser.read(size=n)
    if not rfid:
        rfid = b'default'
    ser.close()
    try:
        out = rfid.decode()
    except:
        rfid = b'default'
        out = rfid.decode()
        
    return out

# Autonomouse 2
#def check_rfid(port, n):
#    """
#    Parameters
#    ----------
#    port : str
#        COM-port of rfid reader.
#    
#    n : int
#        Total number of ID. In this case, it is not used.
#    
#    Return
#    ------
#    out : str
#        ID of mouse present.
#    """
#    
#    ser = serial.Serial(port,
#                        baudrate=19200,
#                        parity=serial.PARITY_NONE,
#                        stopbits=serial.STOPBITS_ONE,
#                        bytesize=serial.EIGHTBITS,
#                        timeout=2)
#    data = b''
#    check = datetime.datetime.now()
#    while True:
#        data += ser.read()
#        if data.endswith(b'\x10\x03'):
#            break
#        if datetime.datetime.now() - check > datetime.timedelta(seconds=2):
#            break
#    ser.close()
#    rfid = data[5:-2]
#    rfid = rfid.replace(b'\x10', b'', 1)
#    if not rfid:
#        out = 'default'
#    elif len(rfid) != 5:
#        out = 'default'
#    else:
#        out = rfid.hex().upper()
#    
#    return out