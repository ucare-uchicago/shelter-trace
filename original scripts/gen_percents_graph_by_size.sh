sizes=(4 8 16 32 64)
traces=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

#array sizes for loops
num_sizes=$((${#sizes[@]} - 1))
num_traces=$((${#traces[@]} - 1))

#size argument means we should look at cumulative I/O size; otherwise look at number of I/Os
size=false

if (($# > 0))
then
    if [ $1 == "size" ]
    then
	size=true
    fi
fi

for s in `seq 0 $num_sizes`
do
    printf -v title "%02d" ${sizes[$s]}
    if "$size"
    then
	graph[$s]=$'set title "PS-'$title'-W: Percent of Data Sheltered, '${sizes[$s]}$'KB Cutoff"\n'
    else
	graph[$s]=$'set title "PIO-'$title'-W: Percent of Requests Sheltered, '${sizes[$s]}$'KB Cutoff"\n'
    fi

    graph[$s]+=$'plot '

    for t in `seq 0 $num_traces`
    do
	ls=$((t+1))
	graph[$s]+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
    done

    for t in `seq 0 $num_traces`
    do
	row=$((2+s))
	ls=$((t+1))
	if "$size"
	then
	    filename=PS${traces[$t]}.txt
	else
	    filename=PIO${traces[$t]}.txt
	fi
	graph[$s]+=$'"'$filename$'\" using 1:'$row$' notitle with lines ls '$ls$',\\\n'
    done

    #remove trailing comma and slash
    graph[$s]=`echo -e "${graph[$s]}" | sed '$ d' | sed '$ s/..$//g'`

    graph[$s]+=$'\nunset title\n'

done

plotlist=""
for s in `seq 0 $num_sizes`
do
    plotlist+=${graph[$s]}
done

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

#set outfile name
if "$size"
then
    eps_out="ps_by_size.eps"
    title="Sheltered Writes as Percentage of Total I/O Size, by Policy"
    ylabel="Percentage of Blocks Sheltered"
else
    eps_out="pio_by_size.eps"
    title="Sheltered Writes as Percentage of Total Number of I/O Requests, by Policy"
    ylabel="Percentage of Requests Sheltered"
fi

outfile="by_size.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,10in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 3,2 title "${title}" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]; set yrange [0:100]

set xlabel "Time (hours)"; set ylabel "${ylabel}"

${linestyles}
${plotlist}
EOF

gnuplot $outfile

rm $outfile