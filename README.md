
If you want to run it on your own machine, the .brev/setup.sh script will install everything you need (in the diffusers conda environment).
To create the same brev environment that runs this API click [here](https://console.brev.dev/environment/new?repo=https://github.com/brevdev/simple-dreambooth-api&instance=g5.2xlarge&diskStorage=100)
In three separate terminal windows run:

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

Then head over to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to run the api.

In the Brev console, you can forward ports. If you go ahead and forward port 8000 - you'll get a public URL and have created your own Dreambooth API!



Much of the code in this implementation was borrowed from [Shivam Shrirao](https://github.com/ShivamShrirao). Huge thanks to him!

