# shelter-trace

## Settings
Before running any scripts, edit the following values in common/settings.py:
* traces_path is the location of the raw traces downloaded directly from http://iotta.snia.org/traces.
  After downloading all traces for a particular workload as a zip file (e.g. RadiusAuthentication.zip)
  extract the zip file into traces_path.
* preprocessed_traces_path is where preprocessed traces are written.
Other scripts will look for preprocessed traces here.
* simulated_traces_path is where simulated traces produced by simulate.py are written
* results_path is where all other results are written.

## Generating simulated traces

Currently simulate.py supports policies B, C and S.
B and C produce simulated traces. Policy S tracks the percent of shelters that are full and the number of times shelters are swapped.
Policy S is not quite done yet.
If you need to simulate policy A, use sim_PA.py.

1. Download your traces from http://iotta.snia.org/traces/158/. Unzip them into the directory defined in traces_path.
2. Preprocess your traces:
    cd preprocess/
    ./preprocess_wrapper.py

This will generate files 1_disk0_consolidated.txt, etc. which are the input files for simulate.py.

3. Run simulate.py once per trace, using the desired sheltering policy:
   cd simulate/
   simulate.py -p {1, 2, 3} -c {B, C} [number]

-p: Preallocation policies. 
* 1: 1 MB shelter every 10 MB
* 2: 5 MB shelter every 50 MB
* 3: 10 MB shelter every 100 MB

-c: Sheltering policies
* B: Don't cleanup, don't shift non-sheltered requests to avoid shelters.
* C: Don't cleanup, do shift non-sheltered requests to avoid shelters.

number: Trace number of the trace we want to process.

Like split_by_disk.py, simulate.py generates a separate output file for each volume in the trace. It also uses the same trace format.
It will generate output files with names
P[p][c]_[n]_disk[i].txt, where p is the preallocation policy, c is the sheltering policy, n is the trace and i is the volume.

For example: Trace 1 has activity on two volumes, disk0 and disk1. 

split_by_disk.py will generate:
* 1_disk0_consolidated.txt
* 1_disk1_consolidated.txt

If we use policy PB3 (don't cleanup, don't shift writes to avoid shelters, one 10MB shelter every 100MB), simulate.py will generate:
* PB3_1_disk0_consolidated.txt
* PB3_1_disk1_consolidated.txt