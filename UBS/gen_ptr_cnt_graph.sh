traces=("T1" "T2" "T3" "T4" "T5" "T6" "T7" "T8" "T9" "T10" "T11" "T12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

num_traces=$((${#traces[@]} - 1))

graph_zoom1+=$'plot '
graph_zoom2+=$'plot '
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    if ((ls != 11))
    then
	graph_zoom1+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
	graph_zoom2+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
    fi
done

for t in `seq 0 $num_traces`
do
    ls=$((t + 1))
    if ((ls != 11))
    then
	filename=PointerCount3_"$ls".txt
	graph_zoom1+=$'"'$filename$'\" using 1:($2 / 1000000) notitle with line ls '$ls$',\\\n'
	graph_zoom2+=$'"'$filename$'\" using 1:($2 / 1000) notitle with line ls '$ls$',\\\n'
    fi
done

graph_zoom1=`echo -e "${graph_zoom1}" | sed '$ d' | sed '$ s/..$//g'`
graph_zoom2=`echo -e "${graph_zoom2}" | sed '$ d' | sed '$ s/..$//g'`

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

eps_out="ptr_cnt.eps"

outfile="ptr_cnt.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 2,1 title "Cumulative Number of Unique Blocks Sheltered" font 'Helvetica, 18'

set autoscale
set key outside
set xdata time
set timefmt "%s"
set format x "%H"
set xrange["0":"86300"]

set xlabel "Time (hours)"
set ylabel "Millions of Unique Blocks Sheltered"

${linestyles}

set title "UBS-32-W-zoom1: Cumulative Number of Unique Blocks Sheltered"
${graph_zoom1}

set ylabel "Thousands of Unique Blocks Sheltered"
set yrange[*:500]
set title "UBS-32-W-zoom2: Cumulative Number of Unique Blocks Sheltered"
${graph_zoom2}

EOF

gnuplot $outfile