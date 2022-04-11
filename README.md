# AutonomouseS

Table of Content:

[TOC]

AutonomouseS is an automatic olfactometer system which was developed as a part of natural-habitat oriented sensor-rich environment maze for laboratory mice. The purpose of AutonomouseS is to train the mice olfactory tasks (e.g. a simple go or no-go task associated to some odours) without the need to remove the mice from the maze. It was developed based on AutonoMouse by Erskine et al.[^1]

[^1]: [Erskine, Andrew et al. “AutonoMouse: High throughput operant conditioning reveals progressive impairment with graded olfactory bulb lesions.” PloS one vol. 14,3 e0211571. 6 Mar. 2019, doi:10.1371/journal.pone.0211571](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6402634/)

## Getting Started

### Hardware

![overview](/Documentation/images/systemOverview.PNG)

The AutonomouseS setup consists of 4 main parts:

1. The lick port and water container.
2. The olfactometer and its tubing system.
3. National Instrument Data Acquisition Board NI-USB 6216 BNC
4. Computer to run the user interfaces (UIs) of the AutonomouseS (*Autonomouse Controller* and *Autonomouse Schedule*)

> **Note** :  
> Only NI-Board NI-USB 6216 BNC is supported by the UI right now.

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

For a detailed user guide in how to use AutonomouseS system for experiment and step-by-step example, click [here](/Documentation/userGuide.md).
