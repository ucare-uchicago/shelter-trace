#!/usr/bin/env python
"""Location of raw and processed traces and other data"""
traces=["LiveMapsBE", "DisplayAdsDataServer", "DisplayAdsPayload", "Exchange", "CFS", "MSNFS", "BuildServer", "DevelopmentToolsRelease", "RadiusAuthentication", "RadiusBackEndSQLServer"]
format_strings=["LiveMapsBE.%m-%d-%Y.%I-%M-%p.trace.etl", "see readme", "see readme", "Exchanged.%m-%d-%Y.%I-%M-%p.trace.etl", "see readme", "see readme", "24.hour.BuildServer.%m-%d-%Y.%I-%M-%p.trace.csv", "TODO", "TODO", "TODO"]
traces_path="/Users/nora/ucare/ucare-data/traces"
preprocessed_traces_path="/Users/nora/ucare/ucare-data/preprocessed-traces"
results_path="/Users/nora/ucare/ucare-data/results"
shelter_size=32  #in all simulations, shelter writes <= 32 KB

