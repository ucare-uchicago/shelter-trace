#Display disks in order in key
#Color better
traces=("T1" "T2" "T3" "T4" "T5" "T6" "T7" "T8" "T9" "T10" "T11" "T12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray", "yellow")

num_traces=$((${#traces[@]} - 1))
max_num_disks=$((${#colors[@]} - 1))

for s in `seq 0 5`
do
    echo ${traces[$s]}
    graph[$s]=$'\n\nset title "PSF-'${traces[$s]}$': Percent of Shelters Full, '${traces[$s]}$'"\n'

    data[$s]=$''
    t=$((s + 1))

    if (( t==5 ))
    then
	graph[$s]+=$'set xtics 3600 \n'
	graph[$s]+=$'set xrange ["0":"21500"] \n'
    fi

    graph[$s]+=$'plot '

    i=0
    for file in SwapSim3_"$t"_*
    do
	i=$((i + 1))
	disknum=`echo $file | sed -E 's/SwapSim3_'$t'_disk([0-9]+).txt/\1/'`
	total_shelters=`cat total_SwapSim3_"$t"_disk"$disknum".txt`
	echo $total_shelters
	graph[$s]+=$'1/0 ls '$i$' title "disk'$disknum$'",\\\n'
	data[$s]+=$'"'$file$'\" every ::1 using 1:(100 * $2 / '$total_shelters$') notitle with lines ls '$i$',\\\n'
    done
    graph[$s]+=${data[$s]}

    #remove trailing ccomma and slash
    graph[$s]=`echo -e "${graph[$s]}" | sed '$ d' | sed '$ s/..$//g'`
done

plotlist1=""
for s in `seq 0 5`
do
    plotlist1+=${graph[$s]}
done


for s in `seq 6 11`
do
    if ((s==10))
    then graph[$s]=""
    else
	echo ${traces[$s]}
	graph[$s]=$'\n\nset title "PSF-'${traces[$s]}$': Percent of Shelters Full, '${traces[$s]}$'"\n'

	data[$s]=$''
	t=$((s + 1))
	if ((t==9))
	then
	    graph[$s]+=$'set xtics 3600 \n'
	    graph[$s]+=$'set xrange ["0":"64800"] \n'
	fi

	if ((t==12))
	then
	    graph[$s]+='set xtics 900 \n'
	    graph[$s]+='set format x "%H:%M" \n'
	    graph[$s]+=$'set xrange [*:*] \n'
	fi

	graph[$s]+=$'plot '
	
	i=0
	for file in SwapSim3_"$t"_*
	do
	    i=$((i + 1))
	    disknum=`echo $file | sed -E 's/SwapSim3_'$t'_disk([0-9]+).txt/\1/'`
	    total_shelters=`cat total_SwapSim3_"$t"_disk"$disknum".txt`
	    graph[$s]+=$'1/0 ls '$i$' title "disk'$disknum$'",\\\n'
	    data[$s]+=$'"'$file$'\" every ::1 using 1:(100 * $2 / '$total_shelters$') notitle with lines ls '$i$',\\\n'
	done
	graph[$s]+=${data[$s]}

        #remove trailing comma and slash
	graph[$s]=`echo -e "${graph[$s]}" | sed '$ d' | sed '$ s/..$//g'`
    fi
done

plotlist2=""
for s in `seq 6 11`
do
    plotlist2+=${graph[$s]}
done

linestyles=""
for s in `seq 1 16`
do
    if ((s < 12 ))
    then
	linestyles+=$'set style line '$s$' lt 1 lw 2 lc rgb "'${colors[$((s-1))]}$'"\n'
    else
	linestyles+=$'set style line '$s$' lt 2 lw 2 lc rgb "'${colors[$((s-12))]}$'"\n'
    fi
done

outfile="full_shelt_percent.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,10in font 'Helvetica, 16' linewidth 2
set output "full_shelt_percent1.eps"
set multiplot layout 3,2 title "Percent of Shelters Full on Each Disk, T1-T6" font 'Helvetica, 18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

${linestyles}

set xlabel "Time (hours)"; set ylabel "Percent of shelters full"

${plotlist1}

unset multiplot

set output "full_shelt_percent2.eps"
set multiplot layout 3,2 title "Percent of Shelters Full on Each Disk, T6-T12" font 'Helvetica, 18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]
set xtics autofreq

${linestyles}

set xlabel "Time (hours)"; set ylabel "Percent of shelters full"


${plotlist2}

EOF

gnuplot $outfile
