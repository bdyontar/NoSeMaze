# User Guide

This documentation is meant to help user navigate the *NoSeMaze Controller* UI and *NoSeMaze Schedule* UI.

## NoSeMaze Controller

### Introduction

The NoSeMaze Controller serves as a central control for the user to start and stop experiment session and save it.

![NoSeMazeControlUI](/Documentation/images/)

#### Experiment Flow

Description of experiment flow goes here.

```mermaid
graph TD
    S[Experiment started]
    SA{Light beam broken?}
    A[Trial/Training defined as in the schedule starts]
    B[Trial/Training ends]
    SV[Already 10 trials?]
    sv[Save experiment]
    SS{Stop button clicked} 
    Z[Stop]

    S --> SA
    SA --> |yes| A
    SA --> |no| SA
    A --> B
    B --> SV
    SV --> |no| SS
    SV --> |yes| sv
    sv --> SS
    SS --> |yes| Z
    SS --> |no| SA

```

### Starting the UI

To start the UI, run *main.py* from the *NoSeMaze Controller* folder using python version 3.10 or above.

> **Important** :  
> The UI is dependent on niDAQmx as it communicates with the NI Board using niDAQmx library. Make sure to install it before starting the UI.

### Starting an Experiment

To start an experiment, there are several things that should be done first.

1. **Populating Animal Table**

    Before starting the experiment, the animal table must be populated first. Click *animal* in the menu bar to open the table.
    </br>

    ![animalWindow](/Documentation/images/)
    </br>

2. **Saving the experiment session**

    After populating the animal table with the animals and its respectives schedules, save the experiment. Click *File* in the menu and save the experiment.
    </br>

    ![savingExperiment](Documentation/images/)
    </br>

3. **Configure the hardware preferences** (optional)

    There might be some configuration that need to be done, such as which analog input channel of the NI board used to detect  
