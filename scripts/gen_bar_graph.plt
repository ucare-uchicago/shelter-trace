set term pos eps enhanced
set style data histogram
set style histogram rowstacked
set style fill solid border -1

set title "PS-All-W"

set ylabel "Percent of total I/O size"
set xlabel "Trace"

set key outside top right title "Size of Request"

set format y "%.0f%%"
set yrange [0:100]
set ytics out nomirror
set xtics nomirror

set output 'ps-w.eps'

plot 'PS-All-W.dat' every ::1 \
     using($2):xtic(1) t "[0, 4KB)" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "[4, 8KB)" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "[8, 16KB)" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "[16, 32KB)" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "[32, 64KB)" lc rgb "orange" lt -1, \
  '' every ::1 using($7) t "{/Symbol=18 \263} 64KB" lc rgb "purple" lt -1