
from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import time
from Sensors.Measurements import MeasObj
from queue import Queue
from Sensors.PlotControl import plotter
from debugpy import debug_this_thread

class MeasurementWorker(QObject):
    """
    Custom worker class to retrieve measurement data

    Attributes:
    -----------
        progress : Signal(int)

        finished : Signal

        measurementsReady : Signal(Queue)
            Signal to emit the measurement result queue

    """
    progress = Signal(int)
    finished = Signal()
    measurementsReady = Signal(Queue)


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
        """_summary_
        """
        self._count = -1
        self._paused = True
        print("Resetting worker")
            
    def _run(self):
        """Method that holds the workers main loop
        """
        self.MeasureObj = MeasObj()
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
                QThread.msleep(1000)

                
            QThread.msleep(100)


class PlotWorker(QObject):
    """Customer Worker class to plot the measurement data
    """
    def __init__(self, graphicsView):

        super().__init__()
        self.graphicsView = graphicsView
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
    def plotMeasurement(self, results_list : list):
        """Slotted method that is called when the plot worker should plot measurement data

        Args:
            results_list (list): List of dictonaries
        """
        self.plotter.plot(results_list)
                
