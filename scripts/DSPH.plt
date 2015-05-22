
set term pos eps enhanced color size 10in,10in font 'Helvetica,16'
set style data histogram
set style histogram rowstacked
set style fill solid border -1
set boxwidth 0.75

set xlabel "Trace"

set key outside top right title "Size of Request"

set format y "%.0f"
set ytics out nomirror
set xtics nomirror

set output 'DSPH.eps'

set multiplot layout 3,2 title "Data Sheltered per Hour"

set ylabel "Data Sheltered (GB)"
set title "DSPH-All-zoom1: Average Data Sheltered per Hour"
plot 'dsph-all.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1


set ylabel "Data Sheltered (GB)"
set title "DSPH-Busy-zoom1: Data Sheltered in Busiest Hour"
plot 'dsph-busy.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1  


set ylabel "Data Sheltered (GB)"
set title "DSPH-All-zoom2: Average Data Sheltered per Hour"
set yrange[0:35]
plot 'dsph-all.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1 


set ylabel "Data Sheltered (GB)"
set title "DSPH-Busy-zoom2: Data Sheltered in Busiest Hour"
set yrange[0:35]
plot 'dsph-busy.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1  

set format y "%.1f

set ylabel "Data Sheltered (GB)"
set title "DSPH-All-zoom3: Average Data Sheltered per Hour"
set yrange[0:1.5]
plot 'dsph-all.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1 

set ylabel "Data Sheltered (GB)"
set title "DSPH-Busy-zoom3: Data Sheltered in Busiest Hour"
set yrange[0:1.5]
plot 'dsph-busy.dat' every ::1 \
     using($2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \
  '' every ::1 using($3) t "(4, 8KB]" lc rgb "green" lt -1, \
  '' every ::1 using($4) t "(8, 16KB]" lc rgb "blue" lt -1, \
  '' every ::1 using($5) t "(16, 32KB]" lc rgb "black" lt -1, \
  '' every ::1 using($6) t "(32, 64KB]" lc rgb "orange" lt -1  


