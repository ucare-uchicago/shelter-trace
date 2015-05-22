
set terminal postscript eps enhanced color size 10in,10in font 'Helvetica,16' linewidth 2
set output "by_size.eps"
set multiplot layout 3,2 title "Cumulative Memory Usage by Small I/O Size" font 'Helvetica,18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

set xlabel "Time (hours)"; set ylabel "Cumulative size in GB"

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

set title "C-04"
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
"T1.txt" using 1:2 notitle with lines ls 1,\
"T2.txt" using 1:2 notitle with lines ls 2,\
"T3.txt" using 1:2 notitle with lines ls 3,\
"T4.txt" using 1:2 notitle with lines ls 4,\
"T5.txt" using 1:2 notitle with lines ls 5,\
"T6.txt" using 1:2 notitle with lines ls 6,\
"T7.txt" using 1:2 notitle with lines ls 7,\
"T8.txt" using 1:2 notitle with lines ls 8,\
"T9.txt" using 1:2 notitle with lines ls 9,\
"T10.txt" using 1:2 notitle with lines ls 10,\
"T11.txt" using 1:2 notitle with lines ls 11,\
"T12.txt" using 1:2 notitle with lines ls 12
unset title
set title "C-08"
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
"T1.txt" using 1:3 notitle with lines ls 1,\
"T2.txt" using 1:3 notitle with lines ls 2,\
"T3.txt" using 1:3 notitle with lines ls 3,\
"T4.txt" using 1:3 notitle with lines ls 4,\
"T5.txt" using 1:3 notitle with lines ls 5,\
"T6.txt" using 1:3 notitle with lines ls 6,\
"T7.txt" using 1:3 notitle with lines ls 7,\
"T8.txt" using 1:3 notitle with lines ls 8,\
"T9.txt" using 1:3 notitle with lines ls 9,\
"T10.txt" using 1:3 notitle with lines ls 10,\
"T11.txt" using 1:3 notitle with lines ls 11,\
"T12.txt" using 1:3 notitle with lines ls 12
unset title
set title "C-16"
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
"T1.txt" using 1:4 notitle with lines ls 1,\
"T2.txt" using 1:4 notitle with lines ls 2,\
"T3.txt" using 1:4 notitle with lines ls 3,\
"T4.txt" using 1:4 notitle with lines ls 4,\
"T5.txt" using 1:4 notitle with lines ls 5,\
"T6.txt" using 1:4 notitle with lines ls 6,\
"T7.txt" using 1:4 notitle with lines ls 7,\
"T8.txt" using 1:4 notitle with lines ls 8,\
"T9.txt" using 1:4 notitle with lines ls 9,\
"T10.txt" using 1:4 notitle with lines ls 10,\
"T11.txt" using 1:4 notitle with lines ls 11,\
"T12.txt" using 1:4 notitle with lines ls 12
unset title
set title "C-32"
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
"T1.txt" using 1:5 notitle with lines ls 1,\
"T2.txt" using 1:5 notitle with lines ls 2,\
"T3.txt" using 1:5 notitle with lines ls 3,\
"T4.txt" using 1:5 notitle with lines ls 4,\
"T5.txt" using 1:5 notitle with lines ls 5,\
"T6.txt" using 1:5 notitle with lines ls 6,\
"T7.txt" using 1:5 notitle with lines ls 7,\
"T8.txt" using 1:5 notitle with lines ls 8,\
"T9.txt" using 1:5 notitle with lines ls 9,\
"T10.txt" using 1:5 notitle with lines ls 10,\
"T11.txt" using 1:5 notitle with lines ls 11,\
"T12.txt" using 1:5 notitle with lines ls 12
unset title
set title "C-64"
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
"T1.txt" using 1:6 notitle with lines ls 1,\
"T2.txt" using 1:6 notitle with lines ls 2,\
"T3.txt" using 1:6 notitle with lines ls 3,\
"T4.txt" using 1:6 notitle with lines ls 4,\
"T5.txt" using 1:6 notitle with lines ls 5,\
"T6.txt" using 1:6 notitle with lines ls 6,\
"T7.txt" using 1:6 notitle with lines ls 7,\
"T8.txt" using 1:6 notitle with lines ls 8,\
"T9.txt" using 1:6 notitle with lines ls 9,\
"T10.txt" using 1:6 notitle with lines ls 10,\
"T11.txt" using 1:6 notitle with lines ls 11,\
"T12.txt" using 1:6 notitle with lines ls 12
unset title

