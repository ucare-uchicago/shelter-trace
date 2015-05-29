# shelter-trace
You will need the following scripts (all found in sim_scripts/) to generate a sheltered trace:
* sort_traces.py -- Sort trace files generated by preprocess_fixed.py by time.
* split_by_disk.py -- Takes traces generated by preprocess_fixed.py and generates a separate trace file for each volume in the original trace.
* config.py -- parses command-line arguments to simulate.py
* simulate.py -- processes trace files generated by split_by_disk.py to generate trace files simulating the effect of I/O sheltering.

Currently simulate.py only supports policies B & C.
If you need to simulate policy A, use sim_PA.py.
Policies D and E have not been implemented yet, although we do keep track of some information needed for cleanup.

## Usage

1. If you're working with traces downloaded directly from http://iotta.snia.org/traces/158, you'll need to preprocess them with preprocess_fixed.py (in the original scripts/ folder). You're probably working with scripts that have already been preprocessed, in which case you can skip this step.
2. From the directory containing your preprocessed traces, run the following once per trace:
python split_by_disk.py n #n is the trace number.
For traces 2, 3, 5 and 6 we need to give the name of the README, because it contains additional information needed to sort the traces:
python split_by_disk.py -r DisplayAdsDataServer 2
python split_by_disk.py -r DisplayAsPayload 3
etc.
(For an example of this, see sim_scripts/all_csds.sh.)
This will generate files 1_disk0.txt, etc. which are the input files for simulate.py.

3. Run simulate.py once per trace, using the desired sheltering policy:
python simulate.py -p {1, 2, 3} -c {B, C} [number]

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
* 1_disk0.txt
* 1_disk1.txt

If we use policy PB3 (don't cleanup, don't shift writes to avoid shelters, one 10MB shelter every 100MB), simulate.py will generate:
* PB3_1_disk0.txt
* PB3_1_disk1.txt