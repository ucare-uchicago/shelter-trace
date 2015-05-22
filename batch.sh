#!/bin/bash -x
traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer")

num_traces=${#traces[@]}

mkdir ../c_results

for i in `seq 1 "$num_traces"`
do
    t=${traces[$((i-1))]}
	./simulate.py -s 10 -r 100 ${t}/Traces/${i}_merged.txt
done