# QSIprep Gear
This gear runs [QSIprep](https://qsiprep.readthedocs.io/) on [BIDS-curated data](https://bids.neuroimaging.io/).

For a description of what QSIprep does, read the [official documentation](https://qsiprep.readthedocs.io/).  

This gear runs the official [`pennbbl/qsiprep:0.15.1` Docker image](https://hub.docker.com/r/pennbbl/qsiprep)

#### __Note__: `DOCKER_HUB` var in `.gitlab-ci.yml` has changed to `false`. By default, this should be set to `true`

# Import Metadata (import-metadata)

## Overview
*{Link To Usage}*

*{Link To FAQ}*

### Summary
`qsiprep` configures pipelines for processing diffusion-weighted MRI (dMRI) data. The main features of this software are

  1. A BIDS-app approach to preprocessing nearly all kinds of modern diffusion MRI data.
  2. Automatically generated preprocessing pipelines that correctly group, distortion correct,
     motion correct, denoise, coregister and resample your scans, producing visual reports and
     QC metrics.
  3. A system for running state-of-the-art reconstruction pipelines that include algorithms
     from Dipy_, MRTrix_, `DSI Studio`_  and others.
  4. A novel motion correction algorithm that works on DSI and random q-space sampling schemes

### Cite
*license:* *{From the "license" section of the manifest}*


*url:* *{From the "url" section of the manifest}*


*cite:* *{From the "cite" section of the manifest}*


### Classification
*Category:* *{From the "custom.gear-builder.category" section of the manifest}*

*Gear Level:*

- [ ] Project
- [x] Subject
- [x] Session
- [ ] Acquisition
- [ ] Analysis

----

[[_TOC_]]

----


### Inputs
This section is autogenerated from the "inputs" section of the manifest

* *{Input-File}*
    - **Name**: *{From "inputs.Input-File"}*
    - **Type**: *{From "inputs.Input-File.base"}*
    - **Optional**: *{From "inputs.Input-File.optional"}*
    - **Classification**: *{Based on "inputs.Input-File.base"}*
    - **Description**: *{From "inputs.Input-File.description"}*
    - **Notes**: *{Any additional notes to be provided by the user}*

  
### Config
This section is autogenerated from the "config" section of the manifest

* *{Config-Option}*
    - **Name**: *{From "config.Config-Option"}*
    - **Type**: *{From "config.Config-Option.type"}*
    - **Description**: *{From "config.Config-Option.description"}*
    - **Default**: *{From "config.Config-Option.default"}*

### Outputs
*{This section is autogenerated from a custom outputs section of the manifest}*

#### Files
*{A list of output files (if possible?)}*

* *{Output-File}*
    - **Name**: *{From "outputs.Input-File"}*
    - **Type**: *{From "outputs.Input-File.base"}*
    - **Optional**: *{From "outputs.Input-File.optional"}*
    - **Classification**: *{Based on "outputs.Input-File.base"}*
    - **Description**: *{From "outputs.Input-File.description"}*
    - **Notes**: *{Any additional notes to be provided by the user}*


#### Metadata
Any notes on metadata created by this gear

### Pre-requisites
This section contains any prerequisites 

#### Prerequisite Gear Runs
A list of gears, in the order they need to be run:

1. ***{Gear-Name}***
    - Level: *{Level at which gear needs to be run}*


#### Prerequisite Files
A list of any files (OTHER than those specified by the input) that the gear will need.
If possible, list as many specific files as you can:

1. ****{File-Name}***
    - Origin: *{Gear-Name, or Scanner, or Upload?}*
    - Level: *{Container level the file is at}*
    - Classification: *{Required classification(s) that the file can be}*


#### Prerequisite Metadata
A description of any metadata that is needed for the gear to run.
If possible, list as many specific metadata objects that are required:

1. ***{Metadata-Key}***
    - Location: *{Nested Metadata Location (info.object1, age, etc)}*
    - Level: *{Container level that metadata is at}*

## Usage
This section provides a more detailed description of the gear, including not just WHAT it does, but HOW it works in flywheel

### Description
*{A detailed description of how the gear works}*

#### File Specifications
This section contains specifications on any input files that the gear may need
##### *{Input-File}*
A description of the input file
    


### Workflow
A picture and description of the workflow


```mermaid
graph LR;
    A[Input-File]:::input --> C;
    C[Upload] --> D[Parent Container <br> Project, Subject, etc];
    D:::container --> E((Gear));
    E:::gear --> F[Analysis]:::container;
    
    classDef container fill:#57d,color:#fff
    classDef input fill:#7a9,color:#fff
    classDef gear fill:#659,color:#fff

```

Description of workflow
1. Upload file to container
1. Select file as input to gear
1. Geat places output in Analysis
    
### Use Cases
This section is very gear dependent, and covers a detailed walkthrough of some use cases.  Should include Screenshots, example files, etc.

#### Use Case 1
***Conditions***:

 -  *{A list of conditons that result in this use case}*
 - [ ] Possibly a list of check boxes indicating things that are absent
 - [x] and things that are present

*{Description of the use case}*

### Logging

An overview/orientation of the logging and how to interperate it.

## FAQ
[FAQ.md](FAQ.md)

## Contributing

[For more information about how to get started contributing to that gear,
checkout [CONTRIBUTING.md](CONTRIBUTING.md).]
