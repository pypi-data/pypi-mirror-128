Package **EmaCalc** implements probabilistic Bayesian analysis
of *Ecological Momentary Assessment (EMA)* data. 
The EMA methodology is used, for example, 
to evaluate the subjective performance of hearing aids or other equipment, 
or the effect of any other kind of psycho-socio-medical intervention,
in the everyday life of the user or client.

## EMA Experiments
In an EMA study, each participant is requested to respond to a questionnaire
during normal everyday life, typically several times per day. 
Some questions may address the current real-life *Scenario*,
i.e., the physical environment and the user's activity and intentions in that situation.
The participant may also be asked to rate, e.g., the pleasantness of aided sound 
or the ease of speech understanding in the current scenario, 
or any other *perceptual Attribute* of interest in the study. 
Typically, many records are collected from each participant, 
but the number of records may vary a lot among respondents.

Thus, EMA data usually include both *nominal* and *ordinal* results.
The analysis model estimates *Attribute* values 
numerically on an objective *interval scale*,
although the raw input data are *subjective*
and indicate only *ordinal* judgments for each Attribute.

This package does *not* include functions to handle the data collection;
it can only use existing files with data recorded earlier.
The package can analyze data from simple or rather complex experimental designs,
including the following features:


1. The complete EMA study may include one or more **Test Stages**,
   for example, *before* and *after* some kind of intervention.

2. Each EMA record may characterize the current situation
   in one or more pre-defined **Scenario Dimensions**. 
    For example, one scenario dimension may be specified
   by the *Common Sound Scenarios (CoSS)* (Wolters et al., 2016),
    which is a list of broad categories of acoustic environments. 
    Other dimensions may specify the *Importance* of the situation,
    and/or the *Hearing-Aid Program* currently used.
    
3. Each EMA record may also include discrete *ratings* for 
   one or more perceptual **Attributes**. 
  For example, one Attribute may be *Speech Understanding*, 
  with ordinal grades *Bad*, *Fair*, *Good*, *Perfect*. 
  Another attribute may be *Comfort*, with grades *Bad*, *Good*.

4. For each *Scenario Dimension*, a list of allowed **Scenario Categories** must be pre-defined. 
    An assessment event is defined by a combination 
    of exactly one selected Category from each Dimension.

5. For each perceptual *Attribute*, a list of discrete ordinal **Attribute Grades**
   must be pre-defined.
         
6. An EMA study may involve one or more distinct **Sub-populations**,
   from which separate groups of participants are recruited.

7. Sub-populations are distinguished by a combination of 
    categories from one or more **Grouping Factors**.
    For example, one factor may be *Age*,
    with categories *Young*, *Middle*, or *Old*.
    Another group factor may be, e.g.,
    *Gender*, with categories *Female*, *Male*, or *Undefined*.

8. The analysis model *does not require* anything about 
    the number of participants from each sub-population,
    or the number of assessments by each participant.
    Of course, the reliability is improved
    if there are many participants from each sub-population, 
    each reporting a large number of EMA records.

## EMA Data Analysis
The analysis model uses the recorded data to
learn a probabilistic model,
representing the statistically most relevant aspects of the data.
The analysis includes a regression model to show how the Attribute values 
are affected by Scenarios. 

1. The analysis results will show predictive **Scenario Profiles** 
    for each sub-population, credible differences between scenario probabilities within each 
    sub-population, and credible differences between sub-populations.

2. The analysis results will also show perceptual **Attribute Values** 
for each sub-population, credible differences between Attribute Values
in separate scenarios, 
and credible Attribute Differences between sub-populations.

The Bayesian analysis automatically estimates the *statistical credibility*
of all analysis results, given the amount of collected data.
The Bayesian model is hierarchical. 
The package can estimate results for

* a *random unseen individual in the (sub-)population* from which the participants were recruited,
* the *(sub-)population mean*,
* each individual *participant*.

## Package Documentation
General information and version history is given in the package doc-string that may be accessed by commands
`import EmaCalc`, `help(EmaCalc)` 
in an interactive Python environment.

Specific information about the organization and accepted formats of input data files
is presented in the doc-string of module cp_data, 
accessible by commands
`import EmaCalc.ema_data`, `help(EmaCalc.ema_data)`.

After running an analysis, the logging output briefly explains
the analysis results presented in figures and tables.

## Usage
1. Install the most recent package version:
    `python3 -m pip install --upgrade EmaCalc`

2. For an introduction to the analysis results and the xlsx input format, 
study, (edit,) and run the included simulation script: `python3 run_sim.py`

3. Copy the template script `run_ema.py`, rename it, and
    edit the copy as suggested in the template, to specify
    - your experimental layout,
    - the top input data directory,
    - a directory where all output result files will be stored.

4. Run your edited script: `python3 run_my_ema.py`

5. In the planning phase, complete analysis results 
may also be calculated for synthetic data 
generated from simulated experiments. 
Simulated experiments allow the same design variants as real experiments.
Copy the template script `run_sim.py`, rename it,
edit the copy, and run your own EMA simulation.

## Requirements
This package requires Python 3.9 or newer,
with recent versions of Numpy, Scipy, and Matplotlib,
as well as a support package samppy, and openpyxl for reading xlsx files.
The pip installer will check and install the required packages if needed.

## References

A. Leijon (2021).
Bayesian Analysis of Ecological Momentary Assessment (EMA) Data 
for Hearing Aid Evaluations. 
*Technical Report with all math details. 
Contact the author for information.*

F. Wolters, K. Smeds, E. Schmidt, and C. Norup (2016).
Common sound scenarios: A context-driven categorization of everyday sound environments
for application in hearing-device research.
*J Amer Acad Audiol*, 27(7):527–540. 
[download](https://www.thieme-connect.de/products/ejournals/abstract/10.3766/jaaa.15105)

K. Smeds, F. Wolters, J. Larsson, P. Herrlin, and M. Dahlquist (2018).
Ecological momentary assessments for evaluation of hearing-aid preference.
*J Acoust Soc Amer* 143(3):1742–1742. [download](https://asa.scitation.org/doi/10.1121/1.5035685)

