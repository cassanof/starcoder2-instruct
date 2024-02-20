OUPUT_DIR="sc2_3b_output"
MODEL="/home/cassano.f/finetuning-harness/model_starcoder2_3b_magicoder/checkpoint-1908"

LANGS="cpp ts js sh"

mkdir -p $OUPUT_DIR

for LANG in $LANGS; do
    CUDA_VISIBLE_DEVICES=0 python eval_instruct.py \
        --model "$MODEL" \
        --output_path "$OUPUT_DIR/${LANG}.jsonl" \
        --language $LANG \
        --temp_dir $OUPUT_DIR | tee "$OUPUT_DIR/${LANG}.log"
done
