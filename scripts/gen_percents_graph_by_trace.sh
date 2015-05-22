sizes=(4 8 16 32 64)
traces=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

#array sizes for loops
num_sizes=$((${#sizes[@]} - 1))
num_traces=$((${#traces[@]} - 1))

#size argument means look at cumulative I/O size; otherwise look at number of requests
size=false
if (($# > 0))
then
    if [ $1 == "size" ]
    then
	size=true
    fi
fi

for t in `seq 0 $num_traces`
do
    num=$((t + 1))

    if "$size"
    then
	graph[$t]=$'set title "PS-T'$num$'-W: Percent of Data Sheltered, T'$num$'"\n'
    else
	graph[$t]=$'set title "PIO-T'$num$'-W: Percent of Requests Sheltered, T'$num$'"\n'
    fi

    if (( num==5 ))
    then
	graph[$t]+=$'set xtics 3600 \n'
	graph[$t]+=$'set xrange ["0":"21500"] \n'
    fi

    if (( num==7 ))
    then
	graph[$t]+=$'set xtics autofreq \n'
	graph[$t]+=$'set xrange["0":"86300"] \n'
    fi

    if (( num==9 ))
    then
	graph[$t]+=$'set xtics 3600 \n'
	graph[$t]+=$'set xrange ["0":"64800"] \n'
    fi

    if (( num==11 ))
    then
#	graph[$t]+=$'set xtics 3600 \n'
	graph[$t]+=$'set xtics 900 \n'
	graph[$t]+=$'set format x "%H:%M" \n'
#	graph[$t]+=$'set xrange ["0":"4600"] \n'
	graph[$t]+=$'set xrange [*:*] \n'
    fi

    graph[$t]+=$'plot '

    for s in `seq 0 $num_sizes`
    do
	ls=$((s+1))
	graph[$t]+=$'1/0 ls '$ls$' title "'${sizes[$s]}$' KB",\\\n'
    done

    for s in `seq 0 $num_sizes`
    do
	row=$((2+s))
	ls=$((s+1))
	if "$size"
	then 
	    filename=PS${traces[$t]}.txt
	else
	    filename=PIO${traces[$t]}.txt
	fi

	graph[$t]+=$'"'$filename$'\" using 1:'$row$' notitle with lines ls '$ls$',\\\n'
    done

    #remove trailing comma and slash
    graph[$t]=`echo -e "${graph[$t]}" | sed '$ d' | sed '$ s/..$//g'`

    graph[$t]+=$'\nunset title\n'

done

plotlist_1=""
plotlist_2=""
for t in `seq 0 5`
do
    plotlist_1+=${graph[$t]}
done

for t in `seq 6 11`
do
    plotlist_2+=${graph[$t]}
done

linestyles=""
for s in `seq 0 $num_sizes`
do
    ls=$((s+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$s]}$'"\n'
done

#set eps outfile name
if "$size"
then
    eps_out="ps_by_trace.eps"
    title="Sheltered Writes as Percentage of Total I/O Size, by Trace"
    ylabel="Percentage of Blocks Sheltered"
else
    eps_out="pio_by_trace.eps"
    title="Sheltered Writes as Percentage of Total Number of I/O Requests, by Trace"
    ylabel="Percentage of Requests Sheltered"
fi

outfile="by_trace.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,10in font 'Helvetica,16' linewidth 2
set output "1_${eps_out}"

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]; set yrange [0:100]
set xlabel "Time (hours)"; set ylabel "${ylabel}"

${linestyles}

set multiplot layout 3,2 title "${title}" font 'Helvetica,18'
${plotlist_1}
unset multiplot
set output "2_${eps_out}"
set multiplot layout 3,2 title "${title}" font 'Helvetica,18'
${plotlist_2}
unset multiplot

EOF

gnuplot $outfile

rm $outfile