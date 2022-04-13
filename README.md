# NoSeMaze

NoSeMaze was developed as an automatic olfactometer system based on AutonoMouse by Erskine et al.[^1] which allows laboratory mice to be trained with olfactory tasks in a semi-natural habitat. This reduced contact between the mice and the experimentator reduces also external influences that might affect the mice as they are training. Since then NoSeMaze was further enriched with many sensors to gather data related to social behaviour of the mice. Hence the name NoSeMaze (natural-habitat oriented sensor-enriched maze).

[^1]: [Erskine, Andrew et al. “AutonoMouse: High throughput operant conditioning reveals progressive impairment with graded olfactory bulb lesions.” PloS one vol. 14,3 e0211571. 6 Mar. 2019, doi:10.1371/journal.pone.0211571](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6402634/)

## Getting Started

### Hardware

![overviewAutoOlfactometer](/Documentation/images/systemOverview.PNG)

The NoSeMaze setup consists of 4 main parts:

1. The automatic olfactometer system, which itself consists of:
    1. a lick port and a water container.
    2. an olfactometer and its tubing system.
    3. a National Instrument Data Acquisition Board NI-USB 6216 BNC
</br>

2. Tube test system, which is used to determine social hierarchy of a mice cohorte.
</br>

3. Ambient sensors, such as temperature sensor, gas sensor, light sensor, etc. to check if there is correlation between the result of the experiment and the environment.
</br>

4. Video cameras which record areas of interest in the NoSeMaze. Video recorded will be used for tracking the mice using DeepLabCut, whereafter the social interactions between the mice are analysed.

> **Note** :  
> Only NI-Board NI-USB 6216 BNC is supported by the UI right now.

These main parts are connected to a computer which controls the experiment and gather the measured data.

For more information about the hardware:

- [Hardware Reference](/Documentation/hardwareReference.md) - Reference to hardware specification

- [Setup Guide](/Documentation/setupGuide.md) - Help by setting up system and some troubleshooting

### Software

This repository consists of 2 main folders:

- Autonomouse Controller &rarr; UI for running experiment
- Autonomouse Schedule &rarr; UI for creating schedule

The UIs are written in **Python** and can be runned directly using python_v3.10+ by running [*main.py*](/Autonomouse%20Controller/main.py) (or [*schedule_main.py*](/Autonomouse%20Schedule/scheduleMain.py)) with the [required python packages](/pythonRequirements.txt) installed. To install the packages required, use the `pip install -r pythonRequirements.txt` or (`pip3 install -r pythonRequirements.txt` on MacOS/Linux).

> **Important** :  
> The UI use PyDAQmx as a python wrapper for niDAQmx library, which is distributed together with the NI Board. Make sure niDAQmx is installed before running the UI.

Software documentations for :

- [Autonomouse Controller](/Autonomouse%20Controller/README.md)
- [Autonomouse Schedule](/Autonomouse%20Schedule/README.md)

## User Guide

For a detailed user guide in how to use NoSeMaze system for experiment and step-by-step example, click [here](/Documentation/userGuide.md).
