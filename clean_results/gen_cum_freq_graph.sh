traces=("T1" "T2" "T3" "T4" "T5" "T6" "T7" "T8" "T9" "T10" "T11" "T12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

num_traces=$((${#traces[@]} - 1))

graph+=$'plot '
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    graph+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
done

for t in `seq 0 $num_traces`
do
    ls=$((t + 1))
    filename=PC3_"$ls"_fill_count.txt
    graph+=$'"'$filename$'\" using 1:2 notitle with line ls '$ls$',\\\n'
done

graph=`echo -e "${graph}" | sed '$ d' | sed '$ s/..$//g'`

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

eps_out="cum_freq.eps"

outfile="cum_freq.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 2,2 title "Cumulative Number of Cleanings" font 'Helvetica, 18'

set autoscale
set key outside
set xdata time
set timefmt "%s"
set format x "%H"
set xrange["0":"86300"]

set xlabel "Time (hours)"
set ylabel "Number of cleanings"

${linestyles}

set yrange[*:12000]
set title "Clean-zoom1: Number of Cleanings Over Time"
${graph}

set yrange[*:1000]
set title "Clean-zoom2: Number of Cleanings Over Time"
${graph}

set yrange[*:100]
set title "Clean-zoom3: Number of Cleanings Over Time"
${graph}

EOF

gnuplot $outfile