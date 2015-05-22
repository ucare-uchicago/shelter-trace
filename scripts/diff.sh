#merge original and new csds into one file
for i in `seq 1 12`
do
    paste -d ' ' CSD"$i".txt PA_CSD"$i".txt | tr -d '\r' | cut -d ' ' -f 1,2,4 > diff"$i".txt
done

#generate graph
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

graph+=$'plot '
for t in `seq 1 12`
do
    graph+=$'1/0 ls '$t$' title "T'$t$'",\\\n'
done

for t in `seq 1 12`
do
    filename=diff"$t".txt
    graph+=$'"'$filename$'\" using 1:(100*(($2-$3)/$2)) notitle with lines ls '$t$',\\\n'
done

#remove trailing comma and slash
graph=`echo -e "${graph}" | sed '$ d' | sed '$ s/..$//g'`


linestyles=""
for t in `seq 1 12`
do
    linestyles+=$'set style line '$t$' lt 1 lw 2 lc rgb "'${colors[$((t-1))]}$'"\n'
done

eps_out="pa_diff.eps"

outfile="pa_diff.plt"


cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,10in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 1,1 font 'Helvetica,18'


set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Percent Cumulative Seek Distance Saved"

${linestyles}

set title "SCSD-PA: Saved Cumulative Seek Distance, Policy A"
${graph}

EOF

gnuplot $outfile

rm $outfile
rm diff*.txt