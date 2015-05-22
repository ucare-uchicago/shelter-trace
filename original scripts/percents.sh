traces=("LiveMapsBE" "DisplayAdsDataServer" "DisplayAdsPayload" "Exchange" "CFS" "MSNFS" "BuildServer" "DevelopmentToolsRelease" "RadiusAuthentication" "RadiusBackEndSQLServer" "TPCC" "TPCE")

num_traces=${#traces[@]}

for i in `seq 1 "$num_traces"`
do
    t=${traces[$((i-1))]}
    echo "$t"
    cp percents.py ../"$t"/Traces/
    cd ../"$t"/Traces/
    if (( (i == 2) || (i == 3) || (i == 5) || (i == 6) ))
    then
	python percents.py -r "$t" "$i"
    elif (( (i == 11) || (i == 12) ))
    then
	python percents.py -t "$i"
    else
	python percents.py "$i"
    fi

    cp PS"$i".txt ../../c_results
    cp PIO"$i".txt ../../c_results

    cd ../../scripts

done