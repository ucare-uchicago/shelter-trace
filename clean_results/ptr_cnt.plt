
set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "ptr_cnt.eps"
set multiplot layout 2,1 title "Cumulative Number of Unique Blocks Sheltered" font 'Helvetica, 18'

set autoscale
set key outside
set xdata time
set timefmt "%s"
set format x "%H"
set xrange["0":"86300"]

set xlabel "Time (hours)"
set ylabel "Millions of Unique Blocks Sheltered"

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


set title "UBS-32-W-zoom1"
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
1/0 ls 12 title "T12",\
"PointerCount3_1.txt" using 1:($2 / 1000000) notitle with line ls 1,\
"PointerCount3_2.txt" using 1:($2 / 1000000) notitle with line ls 2,\
"PointerCount3_3.txt" using 1:($2 / 1000000) notitle with line ls 3,\
"PointerCount3_4.txt" using 1:($2 / 1000000) notitle with line ls 4,\
"PointerCount3_5.txt" using 1:($2 / 1000000) notitle with line ls 5,\
"PointerCount3_6.txt" using 1:($2 / 1000000) notitle with line ls 6,\
"PointerCount3_7.txt" using 1:($2 / 1000000) notitle with line ls 7,\
"PointerCount3_8.txt" using 1:($2 / 1000000) notitle with line ls 8,\
"PointerCount3_9.txt" using 1:($2 / 1000000) notitle with line ls 9,\
"PointerCount3_10.txt" using 1:($2 / 1000000) notitle with line ls 10,\
"PointerCount3_12.txt" using 1:($2 / 1000000) notitle with line ls 12

set ylabel "Thousands of Unique Blocks Sheltered"
set yrange[*:500]
set title "UBS-32-W-zoom2"
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
1/0 ls 12 title "T12",\
"PointerCount3_1.txt" using 1:($2 / 1000) notitle with line ls 1,\
"PointerCount3_2.txt" using 1:($2 / 1000) notitle with line ls 2,\
"PointerCount3_3.txt" using 1:($2 / 1000) notitle with line ls 3,\
"PointerCount3_4.txt" using 1:($2 / 1000) notitle with line ls 4,\
"PointerCount3_5.txt" using 1:($2 / 1000) notitle with line ls 5,\
"PointerCount3_6.txt" using 1:($2 / 1000) notitle with line ls 6,\
"PointerCount3_7.txt" using 1:($2 / 1000) notitle with line ls 7,\
"PointerCount3_8.txt" using 1:($2 / 1000) notitle with line ls 8,\
"PointerCount3_9.txt" using 1:($2 / 1000) notitle with line ls 9,\
"PointerCount3_10.txt" using 1:($2 / 1000) notitle with line ls 10,\
"PointerCount3_12.txt" using 1:($2 / 1000) notitle with line ls 12

