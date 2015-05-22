traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer" "TPCC" "TPCE")

num_traces=${#traces[@]}

for i in `seq 1 "$num_traces"`
do
#    if ( ((i != 1)) && ((i != 7)) && ((i != 11)) && ((i != 12)) )
    if ( ((i == 11)) || ((i == 12)) )
    then
	t=${traces[$((i-1))]}
	echo "$t"
	cp sort_traces.py /Volumes/Awesome\ Files/CS_331/"$t"/Traces
	cp split_by_disk.py /Volumes/Awesome\ Files/CS_331/"$t"/Traces

	cp config.py /Volumes/Awesome\ Files/CS_331/"$t"/Traces
	cp csd_by_disk.py /Volumes/Awesome\ Files/CS_331/"$t"/Traces
	
	cd /Volumes/Awesome\ Files/CS_331/"$t"/Traces
	
	if ( ((i == 2)) || ((i == 3)) || ((i == 5)) || ((i == 6)) )
	then
	    python split_by_disk.py -r "$t" "$i"
	else
	    python split_by_disk.py "$i"
	fi

	python csd_by_disk.py "$i"
	cp "$i"_CSD.txt ~/Desktop/CS/CS331/project/i-o-shelter/graphs/sim_results
	cd ~/Desktop/CS/CS331/project/i-o-shelter/graphs/sim_scripts
    fi
done