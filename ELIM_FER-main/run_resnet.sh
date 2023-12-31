CUDA_VISIBLE_DEVICES=$2 python -m torch.distributed.launch --master_port $3 main.py \
    --project_title aff-wild2 \
    --method $1 \
    --e_lr 5e-5 \
    --r_lr 5e-5 \
    --no_domain 10 \
    --topk 10 \
    --domain_sampling none \
    --online_tracker 0 \
    --tr_batch_size 16 \
    --ermfc_input_dim 512 \
    --ermfc_output_dim 2 \
    --warmup_coef1 5 \
    --warmup_coef2 50 \
    --model resnet18 \
    --save_path /media/backup1/personal_kdh/data/aff_wild2/checkpoint/TEST/ \
    --data_path /media/backup1/personal_kdh/data/aff_wild2/ \
    --vit_path /mlpmixer_checkpoint/INet_1K/Mixer-B_16.npz \
    --print_check 15
