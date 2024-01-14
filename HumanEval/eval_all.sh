OUPUT_DIR="output"
MODEL="/home/cassano.f/finetuning-harness/model_starcoder2_magicoder/checkpoint-636"

LANGS="python cpp java cs php ts js sh"

for LANG in $LANGS; do
    CUDA_VISIBLE_DEVICES=0 python eval_instruct.py \
        --model "$MODEL" \
        --output_path "$OUPUT_DIR/${LANG}.jsonl" \
        --language $LANG \
        --temp_dir $OUPUT_DIR
done
