export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export INSTANCE_DIR="test-training"
export OUTPUT_DIR="trying-full-train-set-output"
eval "$(conda shell.bash hook)"

conda activate diffusers2
# huggingface-cli login

python train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --instance_prompt="a photo of sam" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --learning_rate=5e-6 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=800