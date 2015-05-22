traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer" "TPCC" "TPCE")

num_traces=${#traces[@]}

#run simulator and calculate CSD for each shelter configuration for given code
#copy results to sim_results

for i in `seq 1 "$num_traces"`
do
    if ((i == 11))
    then
	t=${traces[$((i-1))]}
	echo "$t"

	cp simulate.py /Volumes/Awesome\ Files/CS_331/"$t"/Traces
	cd /Volumes/Awesome\ Files/CS_331/"$t"/Traces/
	
	for j in `seq 1 3`
	do
	    python simulate.py  -p "$j" -c "$1" "$i"
	    python csd_by_disk.py -p "$j" -c "$1" "$i"
	    cp P"$1$j"_"$i"_CSD.txt ~/Desktop/CS/CS331/project/i-o-shelter/graphs/sim_results
	done

	cd ~/Desktop/CS/CS331/project/i-o-shelter/graphs/sim_scripts
    fi

done

#plot graph for given code
#cd ../sim_results

#../sim_scripts/merge_and_plot.sh "$1"


