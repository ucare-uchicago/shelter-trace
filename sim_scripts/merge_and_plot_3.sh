#Usage: ./merge_and_plot.sh [policy code] 
#Only plots layout 3

shelter_configs=(3)

colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

for i in "${shelter_configs[@]}"
do

    code=$'P'$1$i

    #merge original and new CSDs into one file

    for t in `seq 1 12`
    do
	paste -d ' ' "$t"_CSD.txt "$code"_"$t"_CSD.txt | tr -d '\r' | cut -d ' ' -f 1,2,4 > diff"$i"_"$t".txt
    done

    #generate graph

    graph[$i]=$'plot '

    for t in `seq 1 12`
    do
	graph[$i]+=$'1/0 ls '$t$' title "T'$t$'",\\\n'
    done

    for t in `seq 1 12`
    do
	filename=diff"$i"_"$t".txt
	graph[$i]+=$'"'$filename$'\" using 1:(100.0*($2-$3)/$2) notitle with lines ls '$t$',\\\n'
    done

    #remove trailing comma and slash
    graph[$i]=`echo -e "${graph[$i]}" | sed '$ d' | sed '$ s/..$//g'`

done

linestyles=""
for t in `seq 1 12`
do
    linestyles+=$'set style line '$t$' lt 1 lw 2 lc rgb "'${colors[$((t-1))]}$'"\n'
done

eps_out="P$1"_diff.eps
outfile="P$1"_diff.plt

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,8in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 2,2 title "Saved Cumulative Seek Distance - Policy ${1}" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Percent of Seek Distance Saved"

${linestyles}

set title "SCSD-P${1}1"
${graph[1]}

set title "SCSD-P${1}2"
${graph[2]}

set title "SCSD-P${1}3"
${graph[3]}

EOF

gnuplot $outfile


#cleanup
for t in `seq 1 12`
do
    for i in `seq 1 3`
    do
	rm diff"$i"_"$t".txt
    done
done

#rm "$outfile"

