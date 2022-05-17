# NoSeMaze

NoSeMaze was developed as an automatic olfactometer system based on AutonoMouse by Erskine et al.[^1] which allows laboratory mice to be trained with olfactory tasks in a semi-natural habitat. Since then NoSeMaze was further enriched with many sensors to gather data related to social behaviour of the mice, hence the name NoSeMaze (natural-habitat oriented sensor-enriched maze).

[^1]: [Erskine, Andrew et al. “AutonoMouse: High throughput operant conditioning reveals progressive impairment with graded olfactory bulb lesions.” PloS one vol. 14,3 e0211571. 6 Mar. 2019, doi:10.1371/journal.pone.0211571](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6402634/). Github Repos: [autonomouse-control](https://github.com/RoboDoig/autonomouse-control), [schedule-generator](https://github.com/RoboDoig/schedule-generator)

## Getting Started

### Hardware

The NoSeMaze setup consists of 4 main modules:

1. The **automatic olfactometer system**, which itself consists of:
    - a lick port and a water container.
    - an olfactometer and its tubing system.
    - a National Instrument Data Acquisition Board NI-USB 6216 BNC

2. **Tube test system**, which is used to determine social hierarchy of a mice cohorte.

3. **Environment sensors module**, which measures temperature, gas, light, etc. to check if there is correlation between the result of the experiment and the environment.

4. **Video cameras** which record areas of interest in the NoSeMaze. Video recorded will be used for tracking the mice using DeepLabCut, whereafter the social interactions between the mice are analysed.

> :memo: **Note** :  
> Only NI-Board NI-USB 6216 BNC is supported by the NoSeMazeControl UI right now.

These main parts are connected to a computer which controls the experiment and gather the measured data.

For more information about the hardware, see the following documentations:

- [Hardware Reference](/Documentation/HardwareDocumentation/hardwareReference.md) - Reference to hardware specification.
- [NoSeMaze Setup](/Documentation/Guides/setupGuide.md) - Overview of the setup and guide to setting up the system, including some information to some troubleshooting.

### Software

This repository consists of 2 main folders:

- NoSeMazeControl &rarr; UI for running experiment.
- NoSeMazeSchedule &rarr; UI for creating schedule used in experiment.

The UIs are written in **Python** and can be runned directly using python v3.10+ by running [*main.py*](/NoSeMazeControl/main.py) in NoSeMazeControl or [*schedule_main.py*](/NoSeMazeSchedule/scheduleMain.py) in NoSeMazeSchedule with the [required python packages](/pythonRequirements.txt) installed. To install the packages required, use the `pip install -r pythonRequirements.txt` or `pip3 install -r pythonRequirements.txt` on MacOS/Linux.

> :exclamation: **Important** :  
> The UI use PyDAQmx as a python wrapper for niDAQmx library, which is distributed together with the NI Board. Make sure niDAQmx is installed before running the UI.

For software documentations of the UI, see [Software Documentation](/Documentation/SoftwareDocumentation/README.md).

## User Guide

For a detailed user guide in how to use NoSeMaze system for experiment and step-by-step example, see [User Guide](/Documentation/Guides/userGuide.md).

## License

NoSeMaze is free software and its documentation is free documentation: you can redistribute it and/or modify it under the terms of GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NoSeMaze. If not, see [https://www.gnu.org/licenses](https://www.gnu.org/licenses).

## Changes From AutonoMouse

NoSeMaze is based on AutonoMouse from Andrew Erskine. Changes that is made to meet our requirements include:

1. Putting `daqface` and `PyPulse` together with `autonomouse-control`.
2. Putting `PyPulse` together with `autonomouse-schedule`.
3. Modifying `DAQ` in `daqface` to support NI USB 6216 BNC
4. Implementing more trials in `daqface` and `ExperimentControl`.
5. Modifying `PyPulse` in `autonomouse-control` and `autonomouse-schedule`.

For a more detailed change log, see [changelog](./Documentation/CHANGELOG.md)
