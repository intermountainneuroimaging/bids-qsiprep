# Release notes

## 1.0.0_0.15.4

__Maintenance__:

Major refactoring, to bring the gear up to the new gear standards in Gitlab:

* Separate parts of the code that are needed to run on a Flywheel instance, rather
than application specific (e.g., where to grab the data, where the outputs should end,
etc.)
* Separate the different parts of the code that are BIDS-app generic from those that
are specific for this App, with the idea that in the future we would work on a BIDS-App
gear class.
* Break the code into smaller functional units, so it is easier to read.
* Try to use auxiliary methods from the Gear Toolkit and bids-client as much as
possible.

## 0.0.1_0.12.2

Initial release, in [GitHub](https://github.com/flywheel-apps/bids-qsiprep/tree/0.0.1_0.12.2)
