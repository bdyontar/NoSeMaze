
scd41_file = ["Temp_RH_CO2", ["Timestamp", "Temp[°C]", "RH[%]", "CO2 [ppm]"]]
apds_file = ["Light", ["Timestamp", "ALS [digits]"]]
spg_file = ["VOC", ["Timestamp", "VOC Raw [digits]", "VOC Index [digits]"]]
mp_file = ["Microphone", ["Timestamp", "Microphone Amplitude [digits]"]]
mics_file = ["NH3", ["Timestamp", "NH3 Sensor resistance [Ohm]"]]

files = [scd41_file, apds_file, spg_file, mp_file, mics_file]

outputfolder = 'csv'

# IDs of the sensornodes
SNIds = [1]

# IDs and COM ports of the sensors
sensor_com_pairs = []


# false if nodes is offline, true if online
node_connected = dict()

# Fixed thresholds for user warning
temp_upper = 19
co2_upper = 100
nh3_upper = 100

sensor_warnings = dict()

