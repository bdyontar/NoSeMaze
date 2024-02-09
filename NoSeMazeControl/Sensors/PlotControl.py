import pyqtgraph as pg
from Sensors import constants
import numpy as np
from datetime import datetime
from queue import Queue


class plotter:
    """Class that contains methods to setup a pyqt plot grid and plot measurement curves

       Attributes
        ----------
        names : list
            List containing measurement ids 

        all_buffers : list
            List containing x,y data buffers

        buffer_size : int 
            Maximum size of each buffer

        curve_items : list
            List to hold the individual curve items
    """
    def __init__(self, graphicsView):

        self.graphicsView = graphicsView
        # Names for the graphs
        self.names = ['sound', 'rh', 'als', 'voc_index', 'voc_raw', 'nh3', 'co2', 'temp']
        self.all_buffers = []
        # How many samples to plot
        self.buffer_size = 2000
        self.curve_items = []

        self.graphicsView.setBackground('w')


    def setupGrid(self):
        """Method to set up a grid layout for plotting.
        Each plot item is added to the graphicView and a list for further handling
        """
        self.graphicsView.clear()
        # Setup the grid layout
        self.plot_sound = self.graphicsView.addPlot(row=0, col=0, labels={'left': 'delta ADC' },title="Microphone")
        self.plot_rh = self.graphicsView.addPlot(row=0, col=1, labels={'left': 'RH (%)' },title="Relative Humidity")
        self.plot_als = self.graphicsView.addPlot(row=1, col=0, labels={'left': 'ALS (lm)' },title="Ambient Light")
        self.plot_voc = self.graphicsView.addPlot(row=1, col=1, labels={'left': 'VoC (ppm)' },title="VoC")
        self.plot_voc_raw = self.graphicsView.addPlot(row=2, col=0, labels={'left': 'VoC Raw (digits)' },title="VoC Raw")
        self.plot_nh3 = self.graphicsView.addPlot(row=2, col=1,labels={'left': 'NH3 (ppm)' },title="NH3")
        self.plot_co2 = self.graphicsView.addPlot(row=3, col=0, labels={'left': 'CO2 (ppm)' },title="CO2")
        self.plot_temp = self.graphicsView.addPlot(row=3, col=1, labels={'left': 'Temp (°C)' },title="Temperature")
        self.plot_widgets = [self.plot_sound, self.plot_rh, self.plot_als, self.plot_voc, 
                        self.plot_voc_raw, self.plot_nh3, self.plot_co2, self.plot_temp]
        

    def initalizeBuffers(self):
        """Method to initalize multidimensional buffers(lists) to hold x,y values to plot.
        One buffer per sensor datastream, and one buffer_t per sensor.
        Additional dimension for each sensornode. 
        """
        n_sensors = len(constants.SNIds)

        # Create a buffer for each measurement
        for data_list_name  in self.names:
            buffer = [[np.nan for _ in range(1)] for _ in range(n_sensors)]
            buffer_t = [[np.nan for _ in range(1)] for _ in range(n_sensors)]

            setattr(self, f'{data_list_name}_buffer', buffer)
            setattr(self, f'{data_list_name}_buffer_t', buffer_t)

        self.all_buffer = [self.sound_buffer, self.rh_buffer, self.als_buffer, self.voc_index_buffer, self.voc_raw_buffer, # type: ignore
                            self.nh3_buffer, self.co2_buffer, self.temp_buffer]# type: ignore
        
        self.all_buffer_t = [self.sound_buffer_t, self.rh_buffer_t, self.als_buffer_t, self.voc_index_buffer_t, self.voc_raw_buffer_t,  # type: ignore
                            self.nh3_buffer_t, self.co2_buffer_t, self.temp_buffer_t]# type: ignore
        
    def createCurves(self):
        """Method to create a plot curve for each sensor result and for each sensor node
        """
        colors = ["r","g","b","m","c"]

        # Create PlotCurveItems and add them to their respective plots
        for name, plot_widget in zip(self.names, self.plot_widgets):

            # Create a legend for each sensor variable
            legend = pg.LegendItem(horSpacing=5)
            legend.setColumnCount(5)
            legend.setLabelTextSize("12pt")
            setattr(self, f'legend_{name}', legend)

            # Create a curve object for each sensor and measurement
            for i in range(0,len(constants.SNIds)):
                curve_item = pg.PlotCurveItem(pen=pg.mkPen(colors[i]))
                curve_id = f'{name}' + f'_{i}'
                setattr(self, f'curve_{curve_id}', curve_item)

                curve_item.setClickable(True)
                curve_item.setToolTip(f'{name}_{i}')
                
                legend.setLabelTextColor(colors[i])

                legend.addItem(curve_item, f"SNID {i+1}")

                self.curve_items.append(curve_item)
                # Add item to respective plot_widget
                plot_widget.addItem(curve_item)

                # Add the Date-time axis
                axis = pg.DateAxisItem(orientation='bottom')
                plot_widget.setAxisItems({'bottom':axis})

        
        self.graphicsView.addItem(legend, row=4, col=0) # type: ignore



    def _trimBuffer(self, buffer : list ,size : int):
        """Trim the buffer to the maximum size for increased plot performance
        Remove the first element if buffer is full

        Args:
            buffer (list): buffer to trim
            size (int): maximum buffer length
        """
        # Remove first element in buffer
        if len(buffer) > size:
            buffer.pop(0)

    # Plot any new sample of each measurement 
    def plot(self,result_list : Queue):
        """Iterates over the result list and adds the new data to the buffer and curves
        Afterwards, trims the buffers to the maximum length

        Args:
            result_list (Queue): list of measurement results
        """
        # If list is not empty
        if result_list.empty() == False:
            res_list = result_list.get()
            
            # Iterate over the results per sensornode
            for i, meas_dict in enumerate(res_list):

                self.data2curve(meas_dict, "curve_sound", "microphone", "sound", i)

                self.data2curve(meas_dict, "curve_als", "apds", "als", i)

                self.data2curve(meas_dict, "curve_temp", "scd41", "temp", i)

                self.data2curve(meas_dict, "curve_co2", "scd41", "co2", i)

                self.data2curve(meas_dict, "curve_rh", "scd41", "rh", i)

                self.data2curve(meas_dict, "curve_nh3", "mics", "nh3", i)

                self.data2curve(meas_dict, "curve_voc_index", "spg", "voc_index", i)

                self.data2curve(meas_dict, "curve_voc_raw", "spg", "voc_raw", i)

                # Trim all buffers
                for buffer in self.all_buffer:
                    self._trimBuffer(buffer[i], self.buffer_size)

                # Trim all buffers
                for buffer_t in self.all_buffer_t:
                    self._trimBuffer(buffer_t[i], self.buffer_size)

    def data2curve(self, dict : dict, curve_name : str, sensor_name : str, variable_name : str, i : int):
        """Add the the buffer values to the plot curves

        Args:
            dict (dict): measurement dictonary
            curve_name (str): name of the curve
            sensor_name (str): name of the sensor
            variable_name (str): variable of the sensor (for example temps)
            i (int): node iterator
        """
        # Get the name of the curve for this node i
        current_curve = getattr(self, f'{curve_name}_{i}')
        # Get the buffer for this parameter and node
        buffer = getattr(self, f'{variable_name}_buffer')
        buffer_t = getattr(self, f'{variable_name}_buffer_t')

        current_time = datetime.now().timestamp()
        # If no new data and first point, append zero
        if (dict[sensor_name]["timestamp"] == -1) & (len(buffer[i]) == 1):
            buffer[i].append(0)
            buffer_t[i].append(current_time)
        # If no new data, append last sample
        elif (dict[sensor_name]["timestamp"] == -1) & (len(buffer[i]) != 1):
            buffer[i].append(buffer[i][len(buffer[i])-1])
            buffer_t[i].append(current_time)
        # If new data, append values
        else:
            self.check_thresholds(dict[sensor_name][variable_name], variable_name)
            buffer[i].append(dict[sensor_name][variable_name])
            buffer_t[i].append(((dict[sensor_name]["timestamp"]))/1000)
            
        current_curve.setData( buffer_t[i] , buffer[i])
        
        
    def check_thresholds(self, value : int, variable_name : str):
        """Method to check if values are outside defined thresholds

        Args:
            value (int): value of measurement
            variable_name (str): name e.g."temp"
        """
        match variable_name:
            case "temp":
                if value > constants.temp_upper:
                    print("Habitat temperature too high")
                    constants.sensor_warnings[variable_name] = value
                else:
                    constants.sensor_warnings[variable_name] = 0
                
            case "nh3":
                if value > constants.nh3_upper:
                    print("Habitat amoniak levels too high")
                    constants.sensor_warnings[variable_name] = value
                else:
                    constants.sensor_warnings[variable_name] = 0

            case "co2":
                if value > constants.co2_upper:
                    print("Habitat CO2 levels too high")
                    constants.sensor_warnings[variable_name] = value
                else:
                    constants.sensor_warnings[variable_name] = 0

                


