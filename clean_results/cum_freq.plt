
set terminal postscript eps enhanced color size 8in,6in font 'Helvetica,16' linewidth 2
set output "cum_freq.eps"
set multiplot layout 2,2 title "Cumulative Number of Cleanings" font 'Helvetica, 18'

set autoscale
set key outside
set xdata time
set timefmt "%s"
set format x "%H"
set xrange["0":"86300"]

set xlabel "Time (hours)"
set ylabel "Number of cleanings"

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


set yrange[*:12000]
set title "Clean-zoom1: Number of Cleanings Over Time"
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
"PC3_1_fill_count.txt" using 1:2 notitle with line ls 1,\
"PC3_2_fill_count.txt" using 1:2 notitle with line ls 2,\
"PC3_3_fill_count.txt" using 1:2 notitle with line ls 3,\
"PC3_4_fill_count.txt" using 1:2 notitle with line ls 4,\
"PC3_5_fill_count.txt" using 1:2 notitle with line ls 5,\
"PC3_6_fill_count.txt" using 1:2 notitle with line ls 6,\
"PC3_7_fill_count.txt" using 1:2 notitle with line ls 7,\
"PC3_8_fill_count.txt" using 1:2 notitle with line ls 8,\
"PC3_9_fill_count.txt" using 1:2 notitle with line ls 9,\
"PC3_10_fill_count.txt" using 1:2 notitle with line ls 10,\
"PC3_11_fill_count.txt" using 1:2 notitle with line ls 11,\
"PC3_12_fill_count.txt" using 1:2 notitle with line ls 12

set yrange[*:1000]
set title "Clean-zoom2: Number of Cleanings Over Time"
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
"PC3_1_fill_count.txt" using 1:2 notitle with line ls 1,\
"PC3_2_fill_count.txt" using 1:2 notitle with line ls 2,\
"PC3_3_fill_count.txt" using 1:2 notitle with line ls 3,\
"PC3_4_fill_count.txt" using 1:2 notitle with line ls 4,\
"PC3_5_fill_count.txt" using 1:2 notitle with line ls 5,\
"PC3_6_fill_count.txt" using 1:2 notitle with line ls 6,\
"PC3_7_fill_count.txt" using 1:2 notitle with line ls 7,\
"PC3_8_fill_count.txt" using 1:2 notitle with line ls 8,\
"PC3_9_fill_count.txt" using 1:2 notitle with line ls 9,\
"PC3_10_fill_count.txt" using 1:2 notitle with line ls 10,\
"PC3_11_fill_count.txt" using 1:2 notitle with line ls 11,\
"PC3_12_fill_count.txt" using 1:2 notitle with line ls 12

set yrange[*:100]
set title "Clean-zoom3: Number of Cleanings Over Time"
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
"PC3_1_fill_count.txt" using 1:2 notitle with line ls 1,\
"PC3_2_fill_count.txt" using 1:2 notitle with line ls 2,\
"PC3_3_fill_count.txt" using 1:2 notitle with line ls 3,\
"PC3_4_fill_count.txt" using 1:2 notitle with line ls 4,\
"PC3_5_fill_count.txt" using 1:2 notitle with line ls 5,\
"PC3_6_fill_count.txt" using 1:2 notitle with line ls 6,\
"PC3_7_fill_count.txt" using 1:2 notitle with line ls 7,\
"PC3_8_fill_count.txt" using 1:2 notitle with line ls 8,\
"PC3_9_fill_count.txt" using 1:2 notitle with line ls 9,\
"PC3_10_fill_count.txt" using 1:2 notitle with line ls 10,\
"PC3_11_fill_count.txt" using 1:2 notitle with line ls 11,\
"PC3_12_fill_count.txt" using 1:2 notitle with line ls 12

