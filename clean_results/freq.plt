
set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "freq.eps"

set autoscale
set key outside
set logscale x 2
set yrange[0:100]

set xlabel "Number of cleanings per shelter"; set ylabel "Cumulative relative frequency (%)"

set style line 1 lt 1 lw 2 lc rgb "red"
set style line 2 lt 1 lw 2 lc rgb "green"
set style line 3 lt 1 lw 2 lc rgb "blue"
set style line 4 lt 1 lw 2 lc rgb "black"
set style line 5 lt 1 lw 2 lc rgb "orange"
set style line 6 lt 1 lw 2 lc rgb "purple"
set style line 7 lt 1 lw 2 lc rgb "brown"
set style line 8 lt 1 lw 2 lc rgb "cyan"
set style line 9 lt 1 lw 2 lc rgb "magenta"
set style line 10 lt 1 lw 2 lc rgb "olive"
set style line 11 lt 1 lw 2 lc rgb "pink"
set style line 12 lt 1 lw 2 lc rgb "slategray"


set title "CleanFreq: Cleaning Frequency per Shelter"

plot 1/0 ls 1 title "T1",\
1/0 ls 2 title "T2",\
1/0 ls 3 title "T3",\
1/0 ls 4 title "T4",\
1/0 ls 5 title "T5",\
1/0 ls 6 title "T6",\
1/0 ls 7 title "T7",\
1/0 ls 8 title "T8",\
1/0 ls 9 title "T9",\
1/0 ls 10 title "T10",\
1/0 ls 11 title "T11",\
1/0 ls 12 title "T12",\
"T1_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 1 pt 7 ps 1,\
"T2_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 2 pt 7 ps 1,\
"T3_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 3 pt 7 ps 1,\
"T4_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 4 pt 7 ps 1,\
"T5_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 5 pt 7 ps 1,\
"T6_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 6 pt 7 ps 1,\
"T7_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 7 pt 7 ps 1,\
"T8_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 8 pt 7 ps 1,\
"T9_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 9 pt 7 ps 1,\
"T10_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 10 pt 7 ps 1,\
"T11_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 11 pt 7 ps 1,\
"T12_cumrelfreq.txt" using 1:($2 * 100) notitle with lp ls 12 pt 7 ps 1

