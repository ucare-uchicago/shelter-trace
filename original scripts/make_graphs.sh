../scripts/gen_graph_by_size.sh
../scripts/gen_graph_by_size.sh read
../scripts/gen_graph_by_size.sh write

../scripts/gen_graph_by_trace.sh
../scripts/gen_graph_by_trace.sh read
../scripts/gen_graph_by_trace.sh write

python ../scripts/printeps.py c_results
