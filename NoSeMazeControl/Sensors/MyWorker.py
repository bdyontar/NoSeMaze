from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import time
from Sensors.Measurements import MeasObj
from queue import Queue
from Sensors.PlotControl import plotter
from debugpy import debug_this_thread

class MeasurementWorker(QObject):
    progress = Signal(int)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._paused = True
        self._count = -1

    def start(self):
        self._paused = False
        if self._count < 0:
            print('Start')
            self._run()
        else:
            print('Continue')

    def stop(self, *, abort=False):
        self._paused = True
        print('Stopping...')

    def getCount(self):
        return self._count
    
    def reset(self):
        self._count = -1
        self._paused = True
        print("Resetting worker")
            
    measurementsReady = Signal(Queue)
    def _run(self):
        
        self.MeasureObj = MeasObj()
        self._count = 0
        self._paused = False

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

    def __init__(self, graphicsView):
        super().__init__()
        self.graphicsView = graphicsView
        self.plotter = plotter(graphicsView)
        self.plotter.setupGrid()
        self.plotter.initalizeBuffers()
        self.plotter.createCurves()

    @Slot()
    def setupPlots(self):
        print("Setting up plots")
        self.plotter.setupGrid()
        self.plotter.initalizeBuffers()
        self.plotter.createCurves()

    @Slot(Queue)
    def plotMeasurement(self, results_list):
        #debug_this_thread()
        self.plotter.plotDict(results_list)
                
