#!/bin/bash
# usage: ./py_eval.sh <path to checkpoints>
if [ -z "$1" ]
  then
    echo "No argument supplied. usage: ./py_eval_1.sh <model> <output>"
    exit 1
fi
if [ -z "$2" ]
  then
    echo "No argument supplied. usage: ./py_eval_1.sh <model> <output>"
    exit 1
fi

LANG="python"
OUPUT_DIR=$2
MODEL=$1

mkdir -p $OUPUT_DIR

echo "Evaluating $MODEL"
python eval_instruct.py \
    --model "$MODEL" \
    --output_path "$OUPUT_DIR/model-${LANG}.jsonl" \
    --language $LANG \
    --temp_dir $OUPUT_DIR | tee "$OUPUT_DIR/model-${LANG}.log"
