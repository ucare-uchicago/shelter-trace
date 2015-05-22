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
    filename=T"$ls"_cumrelfreq.txt
    graph+=$'"'$filename$'\" using 1:($2 * 100) notitle with lp ls '$ls$' pt 7 ps 1,\\\n'
done

graph=`echo -e "${graph}" | sed '$ d' | sed '$ s/..$//g'`

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

eps_out="freq.eps"

outfile="freq.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "${eps_out}"

set autoscale
set key outside
set logscale x 2
set yrange[0:100]

set xlabel "Number of cleanings per shelter"; set ylabel "Cumulative relative frequency (%)"

${linestyles}

set title "CleanFreq: Cleaning Frequency per Shelter"

${graph}

EOF

gnuplot $outfile