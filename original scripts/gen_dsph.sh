ylabel="Data Sheltered (GB)"
title_all=$'DSPH-All'
datafile_all=$'dsph-all.dat'
longtitle_all=$'Average Data Sheltered per Hour'

longtitle_busy=$'Data Sheltered in Busiest Hour'
title_busy=$'DSPH-Busy'
datafile_busy=$'dsph-busy.dat'

plotfile=$'DSPH.plt'

cat > $plotfile <<EOF

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

set ylabel "${ylabel}"
set title "${title_all}-zoom1: ${longtitle_all}"
plot '${datafile_all}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1


set ylabel "${ylabel}"
set title "${title_busy}-zoom1: ${longtitle_busy}"
plot '${datafile_busy}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1  


set ylabel "${ylabel}"
set title "${title_all}-zoom2: ${longtitle_all}"
set yrange[0:35]
plot '${datafile_all}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1 


set ylabel "${ylabel}"
set title "${title_busy}-zoom2: ${longtitle_busy}"
set yrange[0:35]
plot '${datafile_busy}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1  

set format y "%.1f

set ylabel "${ylabel}"
set title "${title_all}-zoom3: ${longtitle_all}"
set yrange[0:1.5]
plot '${datafile_all}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1 

set ylabel "${ylabel}"
set title "${title_busy}-zoom3: ${longtitle_busy}"
set yrange[0:1.5]
plot '${datafile_busy}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1  


EOF

gnuplot $plotfile
