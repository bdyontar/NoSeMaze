
from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import time
from Sensors.Measurements import MeasObj
from Sensors.GravityMeasurements import GravitySensor
from queue import Queue
from Sensors.PlotControl import plotter
from debugpy import debug_this_thread
from Sensors import constants

class MeasurementWorker(QObject):
    """
    Custom worker class to retrieve measurement data.
    Emits a signal when data is retrieved.
    """
    
    measurementsReady = Signal(Queue) 
    """
    A pyqt signal indicating that measurements are ready.

    :param measurementsReady: A queue object representing the measurements.
    :type measurementsReady: Queue

    This signal is used to notify when measurements are available and can be plotted.
    """
    progress = Signal(int)
    """
    A pyqt signal representing the current count

    :param progress: integer count
    :type progress: int
    """
    finished = Signal()
    """
    A pyqt signal emitted when worker is finished
    """
    
    gravityReady = Signal(float)
    

    def __init__(self):
        super().__init__()
        self._paused = True
        self._count = -1

    def start(self):
        """
        Starts the worker if count is zero
        """
        self._paused = False
        if self._count < 0:
            print('Start')
            self._run()
        else:
            print('Continue')

    def stop(self, *, abort=False):
        """
        Stops the worker

        Args:
            abort (bool, optional): Aborts thread. Defaults to False.
        """
        self._paused = True
        print('Stopping...')

    def getCount(self):
        """
        Get current iteration

        Returns:
            int : self._count
        """
        return self._count
    
    def reset(self):
        """Resets the worker
        """
        self._count = -1
        self._paused = True
        print("Resetting worker")
            
    def _run(self):
        """Method that holds the workers main loop
        """
        self.MeasureObj = MeasObj()
        self.GravObj = GravitySensor()
        self._count = 0
        self._paused = False

        # Recieve measurement result queue and emit a signal
        while (True):
            if not self._paused:
                self._count += 1
                self.progress.emit(self._count)

                result = self.MeasureObj.meas_loop()

                try:
                    self.measurementsReady.emit(result)
                except TypeError:
                    pass
                
                if constants.gravity_port:
                    res = self.GravObj.meas_loop()
                    self.gravityReady.emit(res)
                    
                QThread.msleep(1000)

            QThread.msleep(100)


class PlotWorker(QObject):
    """Customer Worker class to plot the measurement data
    """
    def __init__(self, graphicsView, label_NH3):

        super().__init__()
        self.graphicsView = graphicsView
        self.label_NH3 = label_NH3
        self.plotter = plotter(graphicsView)
        self.plotter.setupGrid()
        self.plotter.initalizeBuffers()
        self.plotter.createCurves()

    @Slot()
    def setupPlots(self):
        """Method called when setting up the plot grid, curves and values buffers
        """
        print("Setting up plots")
        self.plotter.setupGrid()
        self.plotter.initalizeBuffers()
        self.plotter.createCurves()

    @Slot(Queue)
    def plotMeasurement(self, results_list : Queue):
        """Slotted method that is called when the plot worker should plot measurement data

        Args:
            results_list (Queue): List of dictonaries
        """
        self.plotter.plot(results_list)
        
    @Slot(float)
    def displayNH3(self, nh3 : float):
        """Slotted method to display the gravity sensor NH3 values as label text

        Args:
            nh3 (float): Current NH3 value
        """
        if constants.gravity_port:
            self.label_NH3.setText("NH3 {} ppm".format(str(nh3)))
            if nh3 > constants.nh3_upper:
                self.label_NH3.setStyleSheet("color: red")
            else:
                self.label_NH3.setStyleSheet("color: green")
