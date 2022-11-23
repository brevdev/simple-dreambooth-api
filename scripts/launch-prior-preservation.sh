eval "$(conda shell.bash hook)"

conda activate diffusers

# Comment this out if you've already done it once:
# huggingface-cli login

# python heictojpg.py "nader"

accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path="stable-diffusion-v1-5"  \
  --pretrained_vae_name_or_path="stable-diffusion-v1-5/vae" \
  --instance_data_dir="nader" \
  --class_data_dir="class_dir" \
  --output_dir="class-based-output" \
  --with_prior_preservation --prior_loss_weight=1.0 \
  --instance_prompt="photo of sksxvs2 man" \
  --class_prompt="photo of a man" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=2 --gradient_checkpointing \
  --learning_rate=5e-6 \
  --use_8bit_adam \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --num_class_images=200 \
  --max_train_steps=800

# python inference.py "fine-tuned-model-output/800" "a photo of Nader wearing sunglasses"