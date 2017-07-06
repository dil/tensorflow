#!/bin/sh
cd tensorflow

if [ ! -f ../cars/tf_files/output_graph.pb ]; then
  echo "Missing cars/tf_files/output_graph.pb"
  exit 1
fi
if [ ! -f ../cars/tf_files/output_labels.txt ]; then
  echo "Missing cars/tf_files/output_labels.txt"
  exit 1
fi

python -m tensorflow.python.tools.optimize_for_inference \
  --input=../cars/tf_files/output_graph.pb \
  --output=../cars/tf_files/output_graph_optimized.pb \
  --input_names="Cast" \
  --output_names="final_result"

python tools/quantization/quantize_graph.py \
  --input=../cars/tf_files/output_graph_optimized.pb \
  --output=../cars/tf_files/output_graph_optimized_rounded.pb \
  --output_node_names=final_result \
  --mode=weights_rounded

cp ../cars/tf_files/output_graph_optimized_rounded.pb ../cars/android/assets/rounded_graph.pb
cp ../cars/tf_files/output_labels.txt ../cars/android/assets/retrained_labels.txt

