# Environment Sensor Module
The Environmental Sensor Module, as provided by Fraunhofer Institute, records different types of sensor-data to gain a better overview of the environmental influence on the animals and vice-versa. The module can be placed on the side wall of the feeding and nesting area. There is an option to install multiple sensor modules for better local accuracy. A single module currently transfers all data values via USB to a provided laptop. Via the User Interface, all time-value graphs for the included sensors can be examined. Using said interface, the user is now able to evaluate incoming data or take further action if needed.
## Sensor Overview
In total, the Environmental Sensor Module consists of five sensors. Each of them performs individual measurements that are calculated and converted to their correlating unit by the microcontroller:
1. A microphone to record noises inside the habitat. The user interface will log the loudest noise within a predefined timespan.
2. A CO2 sensor that logs not only the CO2-concentration (ppm) in the air but also the current temperature (°C) and humidity (RH%).
3. A photodiode to record changes in the light intensity within the habitat. Between each measurement point, only the brightest event is safed.
4. A VOC sensor that provides guiding values for an easier check on air freshness.
5. An ammonia sensor to help with fulfilling hygiene requirements when it comes to animal urination by measuring NH3 in the air (ppm).

![Overview Sensor Elements](/Documentation/_images/EnvironmentalSensorNode.PNG)

## Sensor Usage Information
Over time, some of the sensors might lose accuracy in their measurements. Especially the ammonia sensor will be affected when not callibrated regularly after a few months of usage. Other factors that might have a negative influence on sensor accuracy are:
1. Not giving the sensors enough warm-up time. The ammonia sensor can take up to 8 hours for best accuracy. The VOC sensor might take even more hours to plot first results.
2. High temperatures. When temperatures differ far from the range of 18°C to 28°C, the accuracy of the ammonia sensor might be compromised.
3. High humidity. While it doesn't affect the ammonia sensor as much as temperature, it can still play a role in measurement deviations.
4. High flow rate past the sensors. Both the CO2 sensor and the ammonia sensor will be affected when exposed to a much higher flow rate. When the modules are installed as recommended, this shouldn't be a problem.