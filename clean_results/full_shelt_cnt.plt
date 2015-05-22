
set terminal postscript eps enhanced color size 10in,10in font 'Helvetica, 16' linewidth 2
set output "full_shelt_cnt1.eps"
set multiplot layout 3,2 title "Number of Full Shelters on Each Disk, T1-T6" font 'Helvetica, 18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]

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
set style line 12 lt 2 lw 2 lc rgb "red"
set style line 13 lt 2 lw 2 lc rgb "green"
set style line 14 lt 2 lw 2 lc rgb "blue"
set style line 15 lt 2 lw 2 lc rgb "black"
set style line 16 lt 2 lw 2 lc rgb "orange"


set xlabel "Time (hours)"; set ylabel "Number of full shelters"



set title "NSF-T1: Number of Shelters Full, T1"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
"SwapSim3_1_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_1_disk1.txt" every ::1 using 1:2 notitle with lines ls 2

set title "NSF-T2: Number of Shelters Full, T2"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_2_disk0.txt" every ::1 using 1:2 notitle with lines ls 1

set title "NSF-T3: Number of Shelters Full, T3"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_3_disk0.txt" every ::1 using 1:2 notitle with lines ls 1

set title "NSF-T4: Number of Shelters Full, T4"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
1/0 ls 7 title "disk6",\
1/0 ls 8 title "disk7",\
1/0 ls 9 title "disk8",\
1/0 ls 10 title "disk9",\
"SwapSim3_4_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_4_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_4_disk2.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_4_disk3.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_4_disk4.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_4_disk5.txt" every ::1 using 1:2 notitle with lines ls 6,\
"SwapSim3_4_disk6.txt" every ::1 using 1:2 notitle with lines ls 7,\
"SwapSim3_4_disk7.txt" every ::1 using 1:2 notitle with lines ls 8,\
"SwapSim3_4_disk8.txt" every ::1 using 1:2 notitle with lines ls 9,\
"SwapSim3_4_disk9.txt" every ::1 using 1:2 notitle with lines ls 10

set title "NSF-T5: Number of Shelters Full, T5"
set xtics 3600 
set xrange ["0":"21500"] 
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
1/0 ls 7 title "disk6",\
1/0 ls 8 title "disk7",\
1/0 ls 9 title "disk8",\
"SwapSim3_5_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_5_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_5_disk2.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_5_disk3.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_5_disk4.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_5_disk5.txt" every ::1 using 1:2 notitle with lines ls 6,\
"SwapSim3_5_disk6.txt" every ::1 using 1:2 notitle with lines ls 7,\
"SwapSim3_5_disk7.txt" every ::1 using 1:2 notitle with lines ls 8,\
"SwapSim3_5_disk8.txt" every ::1 using 1:2 notitle with lines ls 9

set title "NSF-T6: Number of Shelters Full, T6"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
"SwapSim3_6_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_6_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_6_disk2.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_6_disk3.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_6_disk4.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_6_disk5.txt" every ::1 using 1:2 notitle with lines ls 6

unset multiplot

set output "full_shelt_cnt2.eps"
set multiplot layout 3,2 title "Number of Full Shelters on Each Disk, T6-T12" font 'Helvetica, 18'

set xdata time
set timefmt "%s"
set format x "%H"

set autoscale
set key outside
set xrange ["0":"86300"]
set xtics autofreq

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
set style line 12 lt 2 lw 2 lc rgb "red"
set style line 13 lt 2 lw 2 lc rgb "green"
set style line 14 lt 2 lw 2 lc rgb "blue"
set style line 15 lt 2 lw 2 lc rgb "black"
set style line 16 lt 2 lw 2 lc rgb "orange"


set xlabel "Time (hours)"; set ylabel "Number of full shelters"




set title "NSF-T7: Number of Shelters Full, T7"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_7_disk0.txt" every ::1 using 1:2 notitle with lines ls 1

set title "NSF-T8: Number of Shelters Full, T8"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk10",\
1/0 ls 4 title "disk11",\
1/0 ls 5 title "disk12",\
1/0 ls 6 title "disk13",\
1/0 ls 7 title "disk14",\
1/0 ls 8 title "disk16",\
1/0 ls 9 title "disk2",\
1/0 ls 10 title "disk3",\
1/0 ls 11 title "disk4",\
1/0 ls 12 title "disk5",\
1/0 ls 13 title "disk6",\
1/0 ls 14 title "disk7",\
1/0 ls 15 title "disk8",\
1/0 ls 16 title "disk9",\
"SwapSim3_8_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_8_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_8_disk10.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_8_disk11.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_8_disk12.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_8_disk13.txt" every ::1 using 1:2 notitle with lines ls 6,\
"SwapSim3_8_disk14.txt" every ::1 using 1:2 notitle with lines ls 7,\
"SwapSim3_8_disk16.txt" every ::1 using 1:2 notitle with lines ls 8,\
"SwapSim3_8_disk2.txt" every ::1 using 1:2 notitle with lines ls 9,\
"SwapSim3_8_disk3.txt" every ::1 using 1:2 notitle with lines ls 10,\
"SwapSim3_8_disk4.txt" every ::1 using 1:2 notitle with lines ls 11,\
"SwapSim3_8_disk5.txt" every ::1 using 1:2 notitle with lines ls 12,\
"SwapSim3_8_disk6.txt" every ::1 using 1:2 notitle with lines ls 13,\
"SwapSim3_8_disk7.txt" every ::1 using 1:2 notitle with lines ls 14,\
"SwapSim3_8_disk8.txt" every ::1 using 1:2 notitle with lines ls 15,\
"SwapSim3_8_disk9.txt" every ::1 using 1:2 notitle with lines ls 16

set title "NSF-T9: Number of Shelters Full, T9"
set xtics 3600 
set xrange ["0":"64800"] 
plot 1/0 ls 1 title "disk0",\
"SwapSim3_9_disk0.txt" every ::1 using 1:2 notitle with lines ls 1

set title "NSF-T10: Number of Shelters Full, T10"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
1/0 ls 7 title "disk6",\
"SwapSim3_10_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_10_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_10_disk2.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_10_disk3.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_10_disk4.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_10_disk5.txt" every ::1 using 1:2 notitle with lines ls 6,\
"SwapSim3_10_disk6.txt" every ::1 using 1:2 notitle with lines ls 7

set title "NSF-T12: Number of Shelters Full, T12"
set xtics 900 
set format x "%H:%M" 
set xrange [*:*] 
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk10",\
1/0 ls 4 title "disk11",\
1/0 ls 5 title "disk12",\
1/0 ls 6 title "disk13",\
1/0 ls 7 title "disk14",\
1/0 ls 8 title "disk15",\
1/0 ls 9 title "disk16",\
1/0 ls 10 title "disk17",\
1/0 ls 11 title "disk18",\
1/0 ls 12 title "disk19",\
1/0 ls 13 title "disk2",\
1/0 ls 14 title "disk8",\
1/0 ls 15 title "disk9",\
"SwapSim3_12_disk0.txt" every ::1 using 1:2 notitle with lines ls 1,\
"SwapSim3_12_disk1.txt" every ::1 using 1:2 notitle with lines ls 2,\
"SwapSim3_12_disk10.txt" every ::1 using 1:2 notitle with lines ls 3,\
"SwapSim3_12_disk11.txt" every ::1 using 1:2 notitle with lines ls 4,\
"SwapSim3_12_disk12.txt" every ::1 using 1:2 notitle with lines ls 5,\
"SwapSim3_12_disk13.txt" every ::1 using 1:2 notitle with lines ls 6,\
"SwapSim3_12_disk14.txt" every ::1 using 1:2 notitle with lines ls 7,\
"SwapSim3_12_disk15.txt" every ::1 using 1:2 notitle with lines ls 8,\
"SwapSim3_12_disk16.txt" every ::1 using 1:2 notitle with lines ls 9,\
"SwapSim3_12_disk17.txt" every ::1 using 1:2 notitle with lines ls 10,\
"SwapSim3_12_disk18.txt" every ::1 using 1:2 notitle with lines ls 11,\
"SwapSim3_12_disk19.txt" every ::1 using 1:2 notitle with lines ls 12,\
"SwapSim3_12_disk2.txt" every ::1 using 1:2 notitle with lines ls 13,\
"SwapSim3_12_disk8.txt" every ::1 using 1:2 notitle with lines ls 14,\
"SwapSim3_12_disk9.txt" every ::1 using 1:2 notitle with lines ls 15

