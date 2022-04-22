"""
This module read the rfid tag of the mouse present at the port.
"""
"""
Copyright (c) 2022 [Insert name here]

This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or 
modify it under the terms of GNU General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with NoSeMaze. If not, see https://www.gnu.org/licenses.
"""

import serial
import datetime


def check_rfid(port, n):
    """
    Read the rfid from the rfid reader with a 2 seconds timeout.
    If no valid rfid read in 2 seconds, returns 'default'.

    Parameters
    ----------
    port : str
        COM-port of rfid reader.

    n : int
        Total number of ID. In this case, it is not used.

    Return
    ------
    out : str
        ID of mouse present.
    """

    ser = serial.Serial(port,
                        baudrate=19200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=2)
    data = b''
    check = datetime.datetime.now()
    while True:
        data += ser.read()
        if data.endswith(b'\x10\x03'):
            break
        if datetime.datetime.now() - check > datetime.timedelta(seconds=2):
            break
    ser.close()
    rfid = data[5:-2]
    rfid = rfid.replace(b'\x10', b'', 1)
    if not rfid:
        out = 'default'
    elif len(rfid) != 5:
        out = 'default'
    else:
        out = rfid.hex().upper()

    return out
