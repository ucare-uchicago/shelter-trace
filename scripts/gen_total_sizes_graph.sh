colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

graph=$'plot '

for t in `seq 1 12`
do
    graph+=$'1/0 ls '$t$' title "T'$t$'",\\\n'
done

for t in `seq 1 12`
do
    filename=All"$t".txt
    graph+=$'"'$filename$'\" using 1:($2/(1024*1024)) notitle with lines ls '$t$',\\\n'
done

#remove trailing comma and slash
graph=`echo -e "${graph}" | sed '$ d' | sed '$ s/..$//g'`


linestyles=""
for t in `seq 1 12`
do
    linestyles+=$'set style line '$t$' lt 1 lw 2 lc rgb "'${colors[$((t-1))]}$'"\n'
done


eps_out="total_sizes.eps"

outfile="total_sizes.plt"

cat > $outfile <<EOF
 
set terminal postscript eps enhanced color size 10in,8in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 2,2 title "Total I/O size" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Total I/O Size (GB)"

${linestyles}

set title "C-all-Size-zoom1: Total I/O size"
${graph}

set yrange [*:500]
set title "C-all-Size-zoom2: Total I/O size"
${graph}

set yrange [*:100]
set title "C-all-Size-zoom3: Total I/O size"
${graph}

EOF

gnuplot $outfile

rm $outfile