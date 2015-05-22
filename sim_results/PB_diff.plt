
set terminal postscript eps enhanced color size 10in,8in font 'Helvetica,16' linewidth 2
set output "PB_diff.eps"
set multiplot layout 2,2 title "Saved Cumulative Seek Distance - Policy B" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Percent of Seek Distance Saved"

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


set title "SCSD-PB1"
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
"diff1_1.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 1,\
"diff1_2.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 2,\
"diff1_3.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 3,\
"diff1_4.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 4,\
"diff1_5.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 5,\
"diff1_6.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 6,\
"diff1_7.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 7,\
"diff1_8.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 8,\
"diff1_9.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 9,\
"diff1_10.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 10,\
"diff1_11.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 11,\
"diff1_12.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 12

set title "SCSD-PB2"
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
"diff2_1.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 1,\
"diff2_2.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 2,\
"diff2_3.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 3,\
"diff2_4.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 4,\
"diff2_5.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 5,\
"diff2_6.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 6,\
"diff2_7.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 7,\
"diff2_8.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 8,\
"diff2_9.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 9,\
"diff2_10.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 10,\
"diff2_11.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 11,\
"diff2_12.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 12

set title "SCSD-PB3"
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
"diff3_1.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 1,\
"diff3_2.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 2,\
"diff3_3.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 3,\
"diff3_4.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 4,\
"diff3_5.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 5,\
"diff3_6.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 6,\
"diff3_7.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 7,\
"diff3_8.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 8,\
"diff3_9.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 9,\
"diff3_10.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 10,\
"diff3_11.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 11,\
"diff3_12.txt" using 1:(100.0*($2-$3)/$2) notitle with lines ls 12

