
set terminal postscript eps enhanced color size 10in,10in font 'Helvetica, 16' linewidth 2
set output "full_shelt_percent1.eps"
set multiplot layout 3,2 title "Percent of Shelters Full on Each Disk, T1-T6" font 'Helvetica, 18'

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


set xlabel "Time (hours)"; set ylabel "Percent of shelters full"



set title "PSF-T1: Percent of Shelters Full, T1"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
"SwapSim3_1_disk0.txt" every ::1 using 1:(100 * $2 / 3283) notitle with lines ls 1,\
"SwapSim3_1_disk1.txt" every ::1 using 1:(100 * $2 / 37940) notitle with lines ls 2

set title "PSF-T2: Percent of Shelters Full, T2"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_2_disk0.txt" every ::1 using 1:(100 * $2 / 1139) notitle with lines ls 1

set title "PSF-T3: Percent of Shelters Full, T3"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_3_disk0.txt" every ::1 using 1:(100 * $2 / 1956) notitle with lines ls 1

set title "PSF-T4: Percent of Shelters Full, T4"
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
"SwapSim3_4_disk0.txt" every ::1 using 1:(100 * $2 / 1051) notitle with lines ls 1,\
"SwapSim3_4_disk1.txt" every ::1 using 1:(100 * $2 / 3849) notitle with lines ls 2,\
"SwapSim3_4_disk2.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 3,\
"SwapSim3_4_disk3.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 4,\
"SwapSim3_4_disk4.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 5,\
"SwapSim3_4_disk5.txt" every ::1 using 1:(100 * $2 / 5285) notitle with lines ls 6,\
"SwapSim3_4_disk6.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 7,\
"SwapSim3_4_disk7.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 8,\
"SwapSim3_4_disk8.txt" every ::1 using 1:(100 * $2 / 5389) notitle with lines ls 9,\
"SwapSim3_4_disk9.txt" every ::1 using 1:(100 * $2 / 5431) notitle with lines ls 10

set title "PSF-T5: Percent of Shelters Full, T5"
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
"SwapSim3_5_disk0.txt" every ::1 using 1:(100 * $2 / 10151) notitle with lines ls 1,\
"SwapSim3_5_disk1.txt" every ::1 using 1:(100 * $2 / 10501) notitle with lines ls 2,\
"SwapSim3_5_disk2.txt" every ::1 using 1:(100 * $2 / 13114) notitle with lines ls 3,\
"SwapSim3_5_disk3.txt" every ::1 using 1:(100 * $2 / 10152) notitle with lines ls 4,\
"SwapSim3_5_disk4.txt" every ::1 using 1:(100 * $2 / 10156) notitle with lines ls 5,\
"SwapSim3_5_disk5.txt" every ::1 using 1:(100 * $2 / 10155) notitle with lines ls 6,\
"SwapSim3_5_disk6.txt" every ::1 using 1:(100 * $2 / 10160) notitle with lines ls 7,\
"SwapSim3_5_disk7.txt" every ::1 using 1:(100 * $2 / 10158) notitle with lines ls 8,\
"SwapSim3_5_disk8.txt" every ::1 using 1:(100 * $2 / 99) notitle with lines ls 9

set title "PSF-T6: Percent of Shelters Full, T6"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
"SwapSim3_6_disk0.txt" every ::1 using 1:(100 * $2 / 516) notitle with lines ls 1,\
"SwapSim3_6_disk1.txt" every ::1 using 1:(100 * $2 / 1149) notitle with lines ls 2,\
"SwapSim3_6_disk2.txt" every ::1 using 1:(100 * $2 / 2673) notitle with lines ls 3,\
"SwapSim3_6_disk3.txt" every ::1 using 1:(100 * $2 / 2251) notitle with lines ls 4,\
"SwapSim3_6_disk4.txt" every ::1 using 1:(100 * $2 / 1910) notitle with lines ls 5,\
"SwapSim3_6_disk5.txt" every ::1 using 1:(100 * $2 / 1910) notitle with lines ls 6

unset multiplot

set output "full_shelt_percent2.eps"
set multiplot layout 3,2 title "Percent of Shelters Full on Each Disk, T6-T12" font 'Helvetica, 18'

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


set xlabel "Time (hours)"; set ylabel "Percent of shelters full"




set title "PSF-T7: Percent of Shelters Full, T7"
plot 1/0 ls 1 title "disk0",\
"SwapSim3_7_disk0.txt" every ::1 using 1:(100 * $2 / 12313) notitle with lines ls 1

set title "PSF-T8: Percent of Shelters Full, T8"
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
"SwapSim3_8_disk0.txt" every ::1 using 1:(100 * $2 / 315) notitle with lines ls 1,\
"SwapSim3_8_disk1.txt" every ::1 using 1:(100 * $2 / 297) notitle with lines ls 2,\
"SwapSim3_8_disk10.txt" every ::1 using 1:(100 * $2 / 1882) notitle with lines ls 3,\
"SwapSim3_8_disk11.txt" every ::1 using 1:(100 * $2 / 2061) notitle with lines ls 4,\
"SwapSim3_8_disk12.txt" every ::1 using 1:(100 * $2 / 1845) notitle with lines ls 5,\
"SwapSim3_8_disk13.txt" every ::1 using 1:(100 * $2 / 327) notitle with lines ls 6,\
"SwapSim3_8_disk14.txt" every ::1 using 1:(100 * $2 / 2231) notitle with lines ls 7,\
"SwapSim3_8_disk16.txt" every ::1 using 1:(100 * $2 / 450) notitle with lines ls 8,\
"SwapSim3_8_disk2.txt" every ::1 using 1:(100 * $2 / 2930) notitle with lines ls 9,\
"SwapSim3_8_disk3.txt" every ::1 using 1:(100 * $2 / 263) notitle with lines ls 10,\
"SwapSim3_8_disk4.txt" every ::1 using 1:(100 * $2 / 102) notitle with lines ls 11,\
"SwapSim3_8_disk5.txt" every ::1 using 1:(100 * $2 / 1895) notitle with lines ls 12,\
"SwapSim3_8_disk6.txt" every ::1 using 1:(100 * $2 / 1871) notitle with lines ls 13,\
"SwapSim3_8_disk7.txt" every ::1 using 1:(100 * $2 / 156) notitle with lines ls 14,\
"SwapSim3_8_disk8.txt" every ::1 using 1:(100 * $2 / 1757) notitle with lines ls 15,\
"SwapSim3_8_disk9.txt" every ::1 using 1:(100 * $2 / 3060) notitle with lines ls 16

set title "PSF-T9: Percent of Shelters Full, T9"
set xtics 3600 
set xrange ["0":"64800"] 
plot 1/0 ls 1 title "disk0",\
"SwapSim3_9_disk0.txt" every ::1 using 1:(100 * $2 / 732) notitle with lines ls 1

set title "PSF-T10: Percent of Shelters Full, T10"
plot 1/0 ls 1 title "disk0",\
1/0 ls 2 title "disk1",\
1/0 ls 3 title "disk2",\
1/0 ls 4 title "disk3",\
1/0 ls 5 title "disk4",\
1/0 ls 6 title "disk5",\
1/0 ls 7 title "disk6",\
"SwapSim3_10_disk0.txt" every ::1 using 1:(100 * $2 / 184) notitle with lines ls 1,\
"SwapSim3_10_disk1.txt" every ::1 using 1:(100 * $2 / 381) notitle with lines ls 2,\
"SwapSim3_10_disk2.txt" every ::1 using 1:(100 * $2 / 573) notitle with lines ls 3,\
"SwapSim3_10_disk3.txt" every ::1 using 1:(100 * $2 / 750) notitle with lines ls 4,\
"SwapSim3_10_disk4.txt" every ::1 using 1:(100 * $2 / 281) notitle with lines ls 5,\
"SwapSim3_10_disk5.txt" every ::1 using 1:(100 * $2 / 813) notitle with lines ls 6,\
"SwapSim3_10_disk6.txt" every ::1 using 1:(100 * $2 / 922) notitle with lines ls 7

set title "PSF-T12: Percent of Shelters Full, T12"
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
"SwapSim3_12_disk0.txt" every ::1 using 1:(100 * $2 / 90) notitle with lines ls 1,\
"SwapSim3_12_disk1.txt" every ::1 using 1:(100 * $2 / 641) notitle with lines ls 2,\
"SwapSim3_12_disk10.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 3,\
"SwapSim3_12_disk11.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 4,\
"SwapSim3_12_disk12.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 5,\
"SwapSim3_12_disk13.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 6,\
"SwapSim3_12_disk14.txt" every ::1 using 1:(100 * $2 / 3619) notitle with lines ls 7,\
"SwapSim3_12_disk15.txt" every ::1 using 1:(100 * $2 / 3619) notitle with lines ls 8,\
"SwapSim3_12_disk16.txt" every ::1 using 1:(100 * $2 / 3619) notitle with lines ls 9,\
"SwapSim3_12_disk17.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 10,\
"SwapSim3_12_disk18.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 11,\
"SwapSim3_12_disk19.txt" every ::1 using 1:(100 * $2 / 3340) notitle with lines ls 12,\
"SwapSim3_12_disk2.txt" every ::1 using 1:(100 * $2 / 386) notitle with lines ls 13,\
"SwapSim3_12_disk8.txt" every ::1 using 1:(100 * $2 / 3619) notitle with lines ls 14,\
"SwapSim3_12_disk9.txt" every ::1 using 1:(100 * $2 / 352) notitle with lines ls 15

