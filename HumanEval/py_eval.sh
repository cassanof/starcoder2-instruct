#!/bin/bash
# usage: ./py_eval.sh <path to checkpoints>
if [ -z "$1" ]
  then
    echo "No argument supplied. usage: ./py_eval.sh <path to checkpoints> <output>"
    exit 1
fi
if [ -z "$2" ]
  then
    echo "No argument supplied. usage: ./py_eval.sh <path to checkpoints> <output>"
    exit 1
fi

LANG="python"
OUPUT_DIR=$2
CHECKPOINT_DIR=$1

mkdir -p $OUPUT_DIR
for dir in $CHECKPOINT_DIR/*/
do
  echo "Evaluating $dir"
  BASENAME=$(basename $dir)
  python eval_instruct.py \
      --model "$dir" \
      --output_path "$OUPUT_DIR/${BASENAME}-${LANG}.jsonl" \
      --language $LANG \
      --temp_dir $OUPUT_DIR | tee "$OUPUT_DIR/${BASENAME}-${LANG}.log"
done
