import base64
from celery import Celery
from fastapi import FastAPI
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, status
from fastapi.exceptions import HTTPException
import aiofiles
import os 
import zipfile
import shutil
from celery.result import AsyncResult
from fastapi.responses import FileResponse


app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired

temporaryZipFileDirectory = './userzipfiles/'

if not os.path.exists(temporaryZipFileDirectory):
    os.makedirs(temporaryZipFileDirectory)

extractedFilesDirectory = './extractedfiles/'
if not os.path.exists(extractedFilesDirectory):
    os.makedirs(extractedFilesDirectory)

outputModelsDirectory = './outputmodels/'
if not os.path.exists(outputModelsDirectory):
    os.makedirs(outputModelsDirectory)

@app.post("/finetune")
async def upload(zipFile: UploadFile = File(...)):
    uuid = uuid4()
    finalOutputDirectory = await saveZipFile(uuid, zipFile)
    outputDirectory = outputModelsDirectory + str(uuid)
    task = train.delay(finalOutputDirectory, outputDirectory)
    # return {"abc": "def"}
    return {"message": f"Job successfully submitted. This should take about 5 minutes to run depending on the queue.", "Task ID": task.id, "Model ID": uuid}

@app.get("/finetunejobstatus")
async def jobStatus(jobid: str):
    result = AsyncResult(jobid, app=celery)
    return result.status

@app.post("/inference")
async def inference(prompt: str, modelId: str):
    modelPath = outputModelsDirectory + modelId + "/" + "800"
    inference.delay(prompt, modelId, modelPath)
    return {"message": "Your inference job has been run. You can get the result by querying the /inferenceoutput endpoint with the task ID.", "Model Id": modelId}
    # os.system('python3 inference.py ' + prompt + ' ' + modelPath)

@app.get("/inferenceoutput")
async def inferenceoutput(modelId: str):
    outputImgPath = f'./{modelId}.png'
    if not os.path.exists(outputImgPath):
        return {"message": "Your training job is still either in the queue or is running. Please try again later."}
    return FileResponse(outputImgPath)

@celery.task
def train(dataDirectory, outputDirectory): # todo: maybe improve the params too
    os.system(f"accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path='CompVis/stable-diffusion-v1-4'  \
  --instance_data_dir={dataDirectory} \
  --output_dir={outputDirectory} \
  --instance_prompt='photo of sks dog' \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --learning_rate=5e-6 \
  --lr_scheduler='constant' \
  --lr_warmup_steps=0 \
  --max_train_steps=800")


@celery.task#(serializer='pickle')
def inference(prompt, modelId, modelPath):
    imgSavePath = f'./{modelId}.png'
    os.system(f'python3 inference.py {modelPath} "{prompt}" {imgSavePath}')

async def saveZipFile(uuid, file):
    try:
        zipFilepath = temporaryZipFileDirectory + str(uuid) + '.zip' # todo: could add a path.join thing here
        print(zipFilepath)
        async with aiofiles.open(zipFilepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='There was an error uploading the file')
    finally:
        await file.close()
    # delete file

    dataDirectory = extractedFilesDirectory + str(uuid)
    if not os.path.exists(dataDirectory):
        os.makedirs(dataDirectory)
    with zipfile.ZipFile(zipFilepath, 'r') as zip_ref:
        zip_ref.extractall(dataDirectory)
    os.remove(zipFilepath)

    # move each .jpg file to the root of the data directory
    finalOutputDirectory = './finaldatadirectory/' + str(uuid)
    if not os.path.exists(finalOutputDirectory):
        os.makedirs(finalOutputDirectory)
    jpgFiles = []
    for root, dirs, files in os.walk(dataDirectory):
        for file in files:
            if file.endswith(".jpg"):
                filePath = os.path.join(root, file)
                shutil.move(filePath, finalOutputDirectory)
                # move filePath to finalOutputDirectory
    shutil.rmtree(dataDirectory)
    return finalOutputDirectory