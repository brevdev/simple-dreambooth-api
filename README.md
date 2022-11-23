This is an api runs Dreambooth on a single node and queues jobs as they come in - though it can easily be ported to multi-node due to the Celery implementation.

## Setup:
- To create the same deployable Brev environment that runs this API click [here](https://console.brev.dev/environment/new?repo=https://github.com/brevdev/simple-dreambooth-api&instance=g5.2xlarge&diskStorage=100)
- If you want to run it on your own machine, the .brev/setup.sh script will install everything you need (in the diffusers conda environment).


## Start the Redis Server:
```
conda activate diffusers
redis-server
```
## Run the Celery worker:
```
conda activate diffusers
celery -A main.celery worker --loglevel=info --concurrency=1
```

## Start the Fast API server:
```
conda activate diffusers
huggingface-cli login
uvicorn main:app --reload
```

Then head over to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to run the api. The finetune route takes in a zip file of images which is used to fine tune Stable Diffusion.

In the Brev console, you can forward ports. If you go ahead and forward port 8000 - you'll get a public URL and have created your own Dreambooth API!



Much of the code in this implementation was borrowed from [Shivam Shrirao](https://github.com/ShivamShrirao). Huge thanks to him!

