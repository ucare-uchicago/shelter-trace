#Settings
Before running any scripts, edit the following values in settings.py:
* traces_path is the location of the raw traces downloaded directly from http://iotta.snia.org/traces.
  After downloading all traces for a particular workload as a zip file (e.g. RadiusAuthentication.zip)
  extract the zip file into traces_path.
* preprocessed_traces_path is where preprocessed traces are written.
All other scripts will look for preprocessed traces here.
* results_path is where all other results are written.
