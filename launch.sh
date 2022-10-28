export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export INSTANCE_DIR="data/dog"
export OUTPUT_DIR="fine-tuned-model-output"
eval "$(conda shell.bash hook)"

conda activate diffusers
huggingface-cli login

accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --instance_prompt="photo of sks dog" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --learning_rate=5e-6 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=800

python inference.py "fine-tuned-model-output/800" "a photo of sks dog wearing sunglasses"