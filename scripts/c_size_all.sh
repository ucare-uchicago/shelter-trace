#!/bin/bash -x
traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer")

num_traces=${#traces[@]}

mkdir ../c_results

for i in `seq 1 "$num_traces"`
do
    t=${traces[$((i-1))]}
    echo "$t"
    cp c_size.py ../"$t"/Traces/
    cd ../"$t"/Traces/
    rm T"$i".txt T"$i"-read.txt T"$i"-write.txt
	#python c_size.py "$i"
	python c_size.py -f write "$i"
	#python c_size.py -f read "$i"

    cp T"$i".txt ../../c_results
    cp T"$i"-read.txt ../../c_results
    cp T"$i"-write.txt ../../c_results

    cd ../../scripts

done