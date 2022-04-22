# Changelog

All notable changes to the project will be documented here. Changes from AutonoMouse are documented under [version 1.0](#10---2022-04-22)

## Unreleased

## [1.0] - 2022-04-22

### Added

**Changes to `autonomouse-control` :**

- Add `PyPulse` in `autonomouse-control`.
- Add `daqface` in `autonomouse-control`.
- Add `Performance` module in `Analysis`.
- Add `Filter` and `Email` module in `HelperFunctions`
- Add `README`s.
- Add e-mailing functionality.
- Add mailing list functionality.
- Add deadman-switch functionality.
- Add crash error message functionality.
- Add rewarding functionalities for two lick ports.

**Changes to `autonomouse-schedule` :**

- Add `PyPulse` in `autonomouse-schedule`
- Add `README`s
- Add custom exception in `Exceptions`

### Changed

**Changes to `autonomouse-control` :**

- Rename AutonoMouse to NoSeMaze.
- Change docstring style von rSt to Numpy.
- Add documentations in source code.
- Add information in `autonomouse-control`'s `README`.
- Change folders containing modules to be modules and the modules to be submodules.
- Implement new trials in `daqface` and `ExperimentControl`.
- Implement a deadman-switch in `ExperimentControl`
- Modify graphics view in analysis window to show correct rejection and correct hit.
- Modify rewarding functions to support NI USB 6216 BNC.
- Modify models in `Experiment` module in `Models` to add custom informations in experiment table, e.g. number of licks.
- Add a maximum limit for rows shown in table view of the experiment table.

**Changes to `autonomouse-schedule` :**

- Rename AutonoMouse to NoSeMaze.
- Rename `main` to `scheduleMain`.
- Rename `Designs` to `ScheduleDesigns`.
- Rename `Models` to `ScheduleModels`.
- Rename `PyPulse` to `SchedulePyPulse`.
- Rename 

### Removed

### Deprecated

**Changes to `autonomouse-control` :**

- E-mailing function is not supported anymore. Messages is saved in cloud folder instead.

**Changes to `autonomouse-schedule` :**

