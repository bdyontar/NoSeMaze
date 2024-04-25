from PyDAQmx import *
from ctypes import *

import numpy
import time
import datetime
import math

import daqface.Utils as Util
from HelperFunctions import Reward as reward

class ThreadSafeDigitalInput:
    """Read thread safe digital input. Used for checking the light beam"""

    def __init__(self, di_device: str, lines: int, secs: float) -> None:
        """
        Parameters
        ----------
        di_device : str
            Name of digital input device

        lines : int
            Number of digital input lines to read.

        secs : float
            Duration of reading data in seconds.
        """

        self.task = Task()

        self.task.CreateDIChan("Dev1/port0/line0", "", DAQmx_Val_ChanPerLine)

        # Array to read samples into
        self.data = numpy.zeros((lines,), dtype=numpy.uint8)
        # Number of samples requested
        self.samples = lines
        # Number of read samples
        self.n = int32()
        

    def DoTask(self):
        """
        Start task and read input.

        Return
        ------
        data : ndarray
            Data measured.
        """

        self.task.StartTask()
        self.task.ReadDigitalLines(self.samples, 1.0, 
            DAQmx_Val_GroupByChannel, self.data, self.samples, byref(self.n), None, None)
        self.ClearTasks()

        values = self.data.tolist()
        print("Digital input values:", values)

        return self.data

    def ClearTasks(self):
        """Stop task and clear it"""

        time.sleep(0.05)
        self.task.StopTask()
        self.task.ClearTask()
        
        

check = ThreadSafeDigitalInput("Dev1", 10, 0.1)
digital_data = check.DoTask()

# Check if any logic highs are contained
contains_ones = numpy.any(digital_data == 1)