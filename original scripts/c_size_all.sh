traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer" "TPCC" "TPCE")

num_traces=${#traces[@]}

mkdir ../c_results

for i in `seq 1 "$num_traces"`
do
    t=${traces[$((i-1))]}
    echo "$t"
    cp c_size.py ../"$t"/Traces/
    cd ../"$t"/Traces/
    if (( (i == 2) || (i == 3) || (i == 5) || (i == 6) ))
    then
	python c_size.py -r "$t" "$i"
	python c_size.py -r "$t" -f write "$i"
	python c_size.py -r "$t" -f read "$i"
    else
	python c_size.py "$i"
	python c_size.py -f write "$i"
	python c_size.py -f read "$i"
    fi

    cp T"$i".txt ../../c_results
    cp T"$i"-read.txt ../../c_results
    cp T"$i"-write.txt ../../c_results

    cd ../../scripts

done