AutoPAMPA: Automated analysis of mass spectrometry quantified assay data for complex mixtures.
=====================

Chad Townsend - University of California Santa Cruz - 2020
---------------------------------------------------
*AutoPAMPA* is a python script designed to process data from PAMPA, partition coefficient, or general chromatographic data acquired from complex mixtures to ease data analysis and increase practical throughput. It accepts mzML format raw data and performs peak-finding, peak bounding, and integration, and peak alignment across paired wells by retention time. Parameters are mainly controlled by a configuration excel file and data is output in excel format as well as (optionally) stacked chromatograms for visual inspection of the automated integration.

More information on *AutoPAMPA* is available in the supporting information of *this* paper (link pending).

The purpose of this readme is to help you install and use *AutoPAMPA* well.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)

    > -   [Required arguments](#required-arguments)
    > -   [Optional arguments](#optional-arguments)
    > -   [Input file preparation](#input-file-preparation)
    > -   [Interpreting output](#interpreting-output)

-   [Known Bugs and Issues](#known-bugs-and-issues)
-   [Bug Reports](#bug-reports)

## Installation:

Run the source code using Python from the command line.

### Requirements:

*AutoPAMPA* requires [poetry](https://python-poetry.org/) and python3.8 to install. After both are installed, simply clone the repo and create a virtual environment with `poetry env use 3.8` then `poetry install --no-dev`. To access the script, navigate to the repository and enter the virtual environment with `poetry shell`. The `autopampa` command comes set up within the shell. It's easiest to perform all jobs in a subdirectory of the repo (as that's where `poetry shell` automatically pulls the right virtual environment). The suggested (ignored) directory is `.data`

## Updates:

The only behavioral change from the previous AutoPAMPA version is that the config file mzml name fields can also be full file paths.

## Usage:

### Required arguments:

*config*: The file path to a specially formatted excel file containing most of the input parameters for *AutoPAMPA*. An example configuration file is included in this repository. A thorough explanation of the parameters contained can be found below.

### Optional arguments:

*-o, --out*: Sets the prefix of the output files (defaults to 'Expt'). This prefix will be applied to both output files as well as any directories created by the -g argument.

*-g, --graph*: Generates stacked extracted ion chromatograms for each target mass for each experiment (well group) and saves them as vector graphics. Generated plots have peaks, bounds, and fit curves labeled. Individual peaks are assigned numbers based on their ordering in the reference well and these labels are added to other wells if successfully aligned and above a peak height threshold (to avoid the worst clutter).

*-u, --gauss*: Activates gaussian integration mode, in which a gaussian is fit to each peak and its parameters used for an exact integration. Default is to simply sum the intensities within the bounds of a peak on the assumption of approximately consistent scan durations (reasonable for simple MS methods in our experience). A code block for taking time differences into account is commented out nearby if this does not hold true for your data.

*-m, --msevents*: Used to unweave alternating event spectra in the case of a multi-event MS method, resolving what would otherwise be jagged peaks. Defaults to 1.

*-i, --ion*: Sets the type of ion to search for. Defaults to proton, but accepts "proton", "sodium", "ammonia" or "H+", "Na+", "NH4+". Can also be set to any floating-point value (including negative ones).

*-v, --verbose:* Sets verbosity level, defaulting to zero. Values 1 or higher causes more messages to be printed and 2 or higher causes the graphic generation to use the smoothed chromatogram (instead of the unsmoothed) to visualize what the gaussian fits are being generated from.


### Input File Preparation:

*AutoPAMPA* expects its main input from an excel configuration file. An example file is included demonstrating the proper format, and is useful as a reference for the sections below. The excel workbook is composed of four sheets: Parameters, Experiment Type, Wells, and Targets.

*AutoPAMPA* uses the pymzml package to read in spectra data from mzML format files. We suggest using [Proteowizard](http://proteowizard.sourceforge.net/)'s msconvert program to convert mass spectrometry data to the mzML format. We used the command line version of msconvert from Proteowizard version 3.0.10577 with some modifiers to strip unnecessary data:
>msconvert --simAsSpectra \*.raw --32 --zlib --filter “peakPicking true 1-“ --filter “zeroSamples removeExtra”

In our hands, including UV data causes pymzml version 0.7.7 to crash, and should therefore be avoided.

#### Parameters
Parameters is composed of settings which are "global" in the sense of affecting the entire job. Formatted as a set of parameter names and values, one set per row, and read in by exact match to their name. All values are expected as floating-point convertible unless otherwise mentioned.

*MZ Precision* should be adjusted to the practical precision of your MS system. If this parameter is set too low, expect to see gaps in extracted ion chromatograms. Set too high, it results in a higher noise level or even phantom peaks.

*Minor Peak Detection Threshold* governs peak detection in the reference well, with all peaks not above the maximum peak height detected multiplied by *this* discarded. Usually set to 0.001 and only rarely adjusted.

*Peak Bound Detection Sensitivity* governs the threshold for rate of change of slope for a peak bound to be called. Usually set at 50 and only rarely adjusted.

*Begin Bound Detection Below Fractional Height* governs the fraction of a peaks maximum height above which bounds cannot be called above. Set to 0.9 by default assuming neat peak shapes, but flat or jagged peak tops may require lowering this significantly at an increasing risk of integrating multiple overlapping peaks as one.

*Maximum Number of Peaks to Report Per Target* expects an integer value. The peak with the lowest intensity is discarded until the maximum number is reached. Used to reduce output of unwanted data.

*Maximum Expected Peak Width (as fraction of run time)* specifies a maximum reasonable peak width beyond which peaks are discarded.

*Savitzky-Golay Smoothing Window* expects an odd integer value, governing the window length of the SG filter. Longer results in more smoothing and should be increased for data with a high scan rate or long run time.

*Savitzky-Golay Smoothing Order* expects an integer value and governs the order of the polynomial fit within the window by the SG filter. A lower value results in more smoothing.

*Retention Time Window* expects two float values separated by a whitespace, representing when to start processing peaks in a run and when to stop (in seconds). Alternatively, an asterisk can be used to represent that the entire run should be processed. Used to reduce output of unwanted data.

*Volume of Donor Well (ml)*, *Volume of Acceptor Well (ml)*, *Active Surface Area of Membrane (cm^2)*, and *Assay Run Time (s)* are experimental parameters of the PAMPA apparatus necessary to the calculation of permeation rate. They are a required part of the configuration file even if solely processing data of other experiment types, but are only accessed for PAMPA experiments.

#### Experiment Type

*AutoPAMPA* can, in addition to processing PAMPA data, also process partition coefficient experimental data, providing automated calculation of ratio and log ratio, or simply be set to integrate peaks and provide the raw integration values.

This worksheet is organized in two columns, one for experiment names (must be unique strings), and one for experiment type. Valid experiment types are "PAMPA", "Ratio", and "Integrate".

#### Wells

This worksheet, organized in six columns, is used to associate well-pairs and mzML files to experiment names. The first column contains the experiment name to associate the rest of the row with and must match a name declared in the Experiment Type worksheet. The second through fourth columns should be filled with file paths (or file names if in the same directory) to appropriate mzML files. 

The second column should contain the file path to a reference well or nothing. The first reference well give for each experiment name is accepted and the rest are ignored. The third and fourth columns are the donor well column and the acceptor well column (or hydrocarbon and water columns for partition coefficient experiments). Well-pairs must be declared in the same row to correctly associate them. If there are multiple well-pairs sharing the same target mass list, they can be associated to the same experiment name (one well-pair per row).

*AutoPAMPA* requires a reference well to be the anchor for peak alignment between associated wells, and, if none is provided, will use the donor well (or well A, column 3) on the assumption that the donor well has greater signal than the acceptor well (or well B, column 4). For a pure integration job, the first well encountered will be assigned as the reference well.

The fifth and sixth columns allow compensation for retention time drift between acquisition of the reference well and the donor and acceptor wells (assuming linear or nearly linear drift). Values should be in seconds.

#### Targets

This worksheet contains 4 columns used to specify the masses of interest for the various experiment names defined in the Experiment Type worksheet. Each row specifies a single exact mass for investigation. As usual, the first column contains the experiment name for the row to be associated with. The second column allows optional association of a name with a target mass (useful for keeping track of internal standards). The third column describes contains the exact masses, which should have enough digits to accomodate the precision defined in *Parameters*.

The final column is an optional location for taking manual control of peak calling and integration bounds of a target mass for an experiment name. Multiple peak locations and bounds can be overwritten per row in the format:
\[Peak, left bound, right bound\]
in seconds without spaces. Multiple sets of these brackets should be separated by whitespace if needed.

Example:
\[110,97,123\] \[543,510,567\]


### Interpreting Output:

*AutoPAMPA* outputs two different excel files after a successful run and (optionally) many vector graphics files that visually represent all integrated peaks. Example output files are also available in this repository. One of the output files is a summary, ending in *_Results.xlsx* and contains averaged results in the case of multiple well-pairs or wells associated with a single experiment name. The other output file ending in *_Out.xlsx* contains the raw integration and calculated statistics for each individual well-pair or well.

Both are output with three worksheets, one for each job type (PAMPA, Ratio, Integrate), and each has its own output format after the first 5 columns, which are universal.

The universal columns are: Experiment name, target mass name, exact mass, peak number, and retention time. Peak number is assigned based on peak alignments to the reference well for a well-set.

PAMPA statistics are calculated as in the [supplemental information](https://pubs.acs.org/doi/suppl/10.1021/acs.jmedchem.8b01259/suppl_file/jm8b01259_si_001.pdf) of Naylor et al. DOI:[10.1021](https://pubs.acs.org/doi/10.1021/acs.jmedchem.8b01259)

Non-detection of a peak in the acceptor well sets permeation rate to zero. 
A %T of over 100% sets permeation rate to "Invalid".

#### Results
This output file is useful for visual inspection of integration through the hyperlinks and an overview of the data.

**PAMPA**
Reported statistics include (in order): The averaged percent transmission, the averaged percent recovery, the averaged permeation rate (10E-6 cm/s), the standard deviation of the permeation rate (if possible), the integrated recovery well intensity, the averaged integrated donor well intensity, the averaged integrated acceptor well intensity, the peak bound retention times, and (if -g) a hyperlink to the relevant stacked trace.

**Ratio**
Reported statistics include (in order): The averaged integrated Well A intensity, the Well A standard deviation (if possible), the averaged integrated Well B intensity, the Well B standard deviation (if possible), the ratio of A/B, the log ratio of A/B, the peak bound retention times, and (if -g) a hyperlink to the relevant stacked trace.

**Integrate**
Reported statistics include (in order): The averaged integrated intensity, the standard deviation of that intensity, the peak bound retention times, and (if -g) a hyperlink to the relevant stacked trace.

#### Out
This output file is useful to examine replicates for bad wells or for analyses that treat well-pairs separately.

**PAMPA**
Reported statistics include (in order): The reference well file path, the reference well integrated intensity, the peak bound retention times, and a set of columns for each well pair. The repeated set contains the donor well file path, the donor well integrated intensity, the acceptor well file path, the acceptor well integrated intensity, the percent transmission, the percent recovery, and the permeation rate (10E-6 cm/s) all for that well-pair.

**Ratio**
Reported statistics include (in order): The reference well file path, the reference well integrated intensity, the peak bound retention times, and a set of columns for each well pair. The repeated set contains the Well A file path, the Well A integrated intensity, the Well B file path, the Well B integrated intensity, and the A/B ratio for that well-pair.

**Integrate**
Reported statistics include (in order): The reference well file path, the reference well integrated intensity, the peak bound retention times, and a set of columns for each well. The repeated set contains each a well's file path and its integrated intensity.

## Known Bugs and Issues:

Non-linear retention time drift between associated wells causes incorrect peak alignments in parts of the run that align poorly.

Currently there is no feature for baseline correction.

## Bug Reports:

Please submit an issue or email me if you find a bug or find part of this Readme unclear!

