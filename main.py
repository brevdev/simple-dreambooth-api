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


app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

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

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    
    uuid = uuid4()
    
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
    
    # extract the zip file then delete it
    dataDirectory = extractedFilesDirectory + str(uuid)
    if not os.path.exists(dataDirectory):
        os.makedirs(dataDirectory)
    with zipfile.ZipFile(zipFilepath, 'r') as zip_ref:
        zip_ref.extractall(dataDirectory)
    # find all .jpg files in the dataDirectory

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
            

    os.remove(zipFilepath)


    outputDirectory = outputModelsDirectory + str(uuid)
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    # then now we can run the actual worker job

    print("Final output directory: " + finalOutputDirectory)
    
    task = train.delay(finalOutputDirectory, outputDirectory)
    return {"message": f"Successfuly uploaded "}



@celery.task#(serializer='pickle')
def train(dataDirectory, outputDirectory):
    print("running command: \n", f"accelerate launch train_dreambooth.py \
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

async def saveZipFile(file):
    uuid = uuid4()
    # check if directory "userzipfiles" exists, if not create it
    if not os.path.exists("./userzipfiles"):
        os.makedirs("./userzipfiles")

    filepath = './userzipfiles/' + str(uuid) + '.zip'
    try:
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='There was an error uploading the file')
    finally:
        await file.close()
    return filepath
@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y