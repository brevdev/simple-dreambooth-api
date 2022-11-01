Much of the code in this implementation was borrowed from [Shivam Shrirao](https://github.com/ShivamShrirao). Huge thanks to him! 

We've pre-configured a Brev environment that'll run Dreambooth out of the box! To get started, hit this [link](https://console.brev.dev/environment/new?setupRepo=https://github.com/brevdev/dreambooth&repo=https://github.com/brevdev/dreambooth&setupPath=.brev/setup.sh&instance=g5.2xlarge) to create a Brev environment. 

## 1) Open your Dreambooth environment:
Open your new DreamBooth environment in VSCode:
```
brev open dreambooth --wait
```
If you don't have the Brev CLI installed, you can install it [here](https://brev.dev/docs/how-to/install-cli).
## 2) Upload training data:
1) Upload about 20 or so photos of someone you want to generate SD samples to the directory (you can drag and drop to vscode)
2) Inside ```launch.sh``` change instance_data_dir to point to your training data (line 12)
3) Then change the prompts you use on lines 13 and 22 of launch.sh e.g. "a photo of Jeremy" & "a photo of Jeremy wearing sunglasses"

## 3) Run the training job:
Setup your HuggingFace token:
```
huggingface-cli login
```
It'll prompt you to add your huggingface token (make sure you've accepted the Hugging Face [license agreement](https://huggingface.co/CompVis/stable-diffusion-v1-4)).

Then run the training job :
```
sh launch.sh
```
(this should take about 5 minutes)
## 4) Generate samples:
To then do your own inference run:
```
conda activate diffusers
python inference.py "fine-tuned-model-output/800" "a photo of sks dog wearing sunglasses"
```

To check out all the things you can do, take a look at [Shivam's example](https://github.com/ShivamShrirao/diffusers/tree/main/examples/dreambooth)
