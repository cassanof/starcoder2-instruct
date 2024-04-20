if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Please give deepspeed config file as argument"
    exit 1
fi
DS=$(realpath $1)
export WANDB_PROJECT="sc2-instruct"
export WANDB_NAME=$(basename $0 .sh)
python3 -m torch.distributed.launch \
        --nproc_per_node 8 \
        main.py \
        --deepspeed="$DS" \
        --model_path="bigcode/starcoder2-15b" \
        --dataset_name="cassanof/sc2-oss-instruct-50k" \
        --dataset_loader="padded" \
        --mask_loss_till_token_id 7 \
        --no_approx_tokens \
        --output_dir="./model_sc2_self_oss_instruct" \
        --seq_length 4096 \
        --epochs 5 \
        --fa2 \
        --batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 1e-5 \
        --num_warmup_steps 15 \
        --attention_dropout 0.1 \
        --num_workers=$(expr $(nproc --all) - 4) \
        --no_fp16 \
        --bf16 \
        --eval_freq 0.0 \
        --perc_valid_set 0.0 \
        --save_total_limit 20
