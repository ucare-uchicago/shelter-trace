ylabel="Percent of total I/O size"
title=$'PS-All-'
longtitle=$'as Percentage of Total I/O Size'
if [ $1 == "count" ]
then
    ylabel="Percent of total I/O requests"
    longtitle=$'as Percentage of All I/O Requests'
    title=$'PIO-All-'
fi


if [ $2 == "read" ]
then
    title+=$'R'
    longtitle=$'Read Request Size Distribution '$longtitle
else
    title+=$'W'
    longtitle=$'Write Request Size Distribution '$longtitle
fi
    
plotfile=$title$'.plt'
datafile=$title$'.dat'

cat > $plotfile <<EOF

set term pos eps enhanced color size 8in,5in font 'Helvetica,24'
set style data histogram
set style histogram rowstacked
set style fill solid border -1
set boxwidth 0.75

set title "${title}: ${longtitle}"

set ylabel "${ylabel}"
set xlabel "Trace"

set key outside top right title "Size of Request"

set format y "%.0f%%"
set yrange [0:100]
set ytics out nomirror
set xtics nomirror

set output '${title}.eps'

plot '${datafile}' every ::1 \\
     using(\$2):xtic(1) t "(0, 4KB]" lc rgb "red" lt -1, \\
  '' every ::1 using(\$3) t "(4, 8KB]" lc rgb "green" lt -1, \\
  '' every ::1 using(\$4) t "(8, 16KB]" lc rgb "blue" lt -1, \\
  '' every ::1 using(\$5) t "(16, 32KB]" lc rgb "black" lt -1, \\
  '' every ::1 using(\$6) t "(32, 64KB]" lc rgb "orange" lt -1, \\
  '' every ::1 using(\$7) t "> 64KB" lc rgb "purple" lt -1

EOF

gnuplot $plotfile
