size=32
traces=("T3" "T8" "T10")
names=("DAP-PS" "DTRS" "RAD-BE")
colors=("red" "green" "blue")

#array sizes for loops
num_traces=$((${#traces[@]} - 1))


#set ymax manually because TPCC sucks
ymax=220

printf -v title "%02d" $size

graph=$'set title "Cumulative Memory Usage By Trace ({/Symbol \243} 32 KB Write)" \n'

graph+=$'plot '

for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    graph+=$'1/0 ls '$ls$' title "'${names[$t]}$'" ,\\\n'
done

for t in `seq 0 $num_traces`
do
    row=5
    ls=$((t+1))
    filename=${traces[$t]}-write.txt
    graph+=$'"'$filename$'\" using 1:'$row$' notitle with lines ls '$ls$',\\\n'
done

graph=`echo -e "$graph" | sed '$ d' | sed '$ s/..$//g'`

linestyles=""
for t in `seq 0 $num_traces`
do
    ls=$((t+1))
    linestyles+=$'set style line '$ls$' lt 1 lw 2 lc rgb "'${colors[$t]}$'"\n'
done

eps_out="graph_for_knot.eps"

outfile="knot_graph.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 6in,5in font 'Helvetica,30' linewidth 2
set output "${eps_out}"

set xdata time
set timefmt "%s"
set format x "%H"

set xtics 14400
set ytics 4

set autoscale
set key left top
set xrange ["0":"86200"]

set xlabel "Time (hours)"; set ylabel "Cumulative size in GB" offset 2

${linestyles}
${graph}
EOF

gnuplot $outfile

rm $outfile