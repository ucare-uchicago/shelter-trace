sizes=(4 8 16 32 64)
traces=("T1" "T2" "T3" "T4" "T5" "T6" "T7" "T8" "T9" "T10" "T11" "T12")
colors=("red" "green" "blue" "black" "orange" "purple" "brown" "cyan" "magenta" "olive" "pink" "slategray")

#array sizes for loops
num_sizes=$((${#sizes[@]} - 1))
num_traces=$((${#traces[@]} - 1))

#read/write filter
read_f=false
write_f=false
if (($# > 0))
then
    if [ $1 == "read" ]
    then
	read_f=true
    elif [ $1 == "write" ]
    then
	write_f=true
    fi
fi

#set ymax manually because TPCC sucks
if "$read_f"
then
    ymax=(20 200 200 220 500)
elif "$write_f"
then
    ymax=(40 140 150 200 260)
else
    ymax=(40 300 350 400 550)
fi


for s in `seq 0 $num_sizes`
do
    printf -v title "%02d" ${sizes[$s]}
    if "$read_f"
    then
	graph[$s]=$'set title "C-'$title'-R: Cumulative Small Read Size, '${sizes[$s]}$'KB Cutoff"\n'
    elif "$write_f"
    then
	graph[$s]=$'set title "C-'$title'-W: Cumulative Small Write Size, '${sizes[$s]}$'KB Cutoff"\n'
    else
	graph[$s]=$'set title "C-'$title$': Cumulative Small I/O Size, '${sizes[$s]}$'KB Cutoff"\n'
    fi

    graph[$s]+=$'set yrange [0:'${ymax[$s]}']\n'
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
	if "$read_f"
	then
	    filename=${traces[$t]}-read.txt
	elif "$write_f"
	then
	    filename=${traces[$t]}-write.txt
	else
	    filename=${traces[$t]}.txt
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
if "$read_f"
then
    title="(Reads)"
    eps_out="reads_by_size.eps"
elif "$write_f"
then
    title="(Writes)"
    eps_out="writes_by_size.eps"
else
    title=""
    eps_out="by_size.eps"
fi

outfile="by_size.plt"

cat > $outfile <<EOF

set terminal postscript eps enhanced color size 10in,10in font 'Helvetica,16' linewidth 2
set output "${eps_out}"
set multiplot layout 3,2 title "Cumulative Memory Usage by Policy ${title}" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Cumulative size in GB"

${linestyles}
${plotlist}
EOF

gnuplot $outfile

rm $outfile