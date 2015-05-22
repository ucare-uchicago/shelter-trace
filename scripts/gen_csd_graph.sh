sizes=(4 8 16 32 64)
traces=("T1" "T2" "T3" "T4" "T5" "T6" "T7" "T8" "T9" "T10" "T11" "T12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

#array sizes for loops
num_sizes=$((${#sizes[@]} - 1))
num_traces=$((${#traces[@]} - 1))

#graph=$'set title "CSD"\n'
graph+=$'plot '
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    graph+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
done

for t in `seq 0 $num_traces`
do
    row=$((2+s))
    ls=$((t+1))
    filename=CSD"$ls".txt
#    graph+=$'"'$filename$'\" using 1:($'$row$'/2199023255552) notitle with lines ls '$ls$',\\\n'
    graph+=$'"'$filename$'\" using 1:($'$row$'/2251799813685248) notitle with lines ls '$ls$',\\\n'
done

#remove trailing comma and slash
graph=`echo -e "${graph}" | sed '$ d' | sed '$ s/..$//g'`

#graph_small=$'set title "CSD"\n'
#graph_small+=$'plot '
#for t in `seq 0 $num_traces`
#do
#    ls=$((t+1))
#    graph_small+=$'1/0 ls '$ls$' title "'${traces[$t]}$'",\\\n'
#done

#for t in `seq 0 $num_traces`
#do
#    row=$((2+s))
#    ls=$((t+1))
#    filename=CSD"$ls".txt
#    graph_small+=$'"'$filename$'\" using 1:($'$row$'/1000000000000) notitle with lines ls '$ls$',\\\n'
#done

#remove trailing comma and slash
#graph_small=`echo -e "${graph_small}" | sed '$ d' | sed '$ s/..$//g'`

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

eps_out="csd.eps"

outfile="csd.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,8in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 2,2 title "Cumulative Seek Distance" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Cumulative Seek Distance (Exabytes)"

${linestyles}

set title "CSD-zoom1: Cumulative Seek Distance"
${graph}

set yrange [*:2]
set title "CSD-zoom2: Cumulative Seek Distance"
${graph}

set yrange [*:.02]
set title "CSD-zoom3: Cumulative Seek Distance"
${graph}

EOF

gnuplot $outfile

rm $outfile