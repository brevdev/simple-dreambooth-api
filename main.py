import base64
from celery import Celery
from fastapi import FastAPI
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, status
from fastapi.exceptions import HTTPException
import aiofiles
import os 

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


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # convert file to bytes
    
    # print("file is:")
    # print(file)
    # task = train.delay(data)
    # create a uuid for the user request
    # uuid = uuid4()
    # # # check if directory "userzipfiles" exists, if not create it
    # if not os.path.exists("./userzipfiles"):
    #     os.makedirs("./userzipfiles")
    # try:
    #     print("abc")
    #     filepath = './userzipfiles/' + str(uuid) + '.zip'
    #     print(filepath)
    #     async with aiofiles.open(filepath, 'wb') as f:
    #         while chunk := await file.read(CHUNK_SIZE):
    #             await f.write(chunk)
    # except Exception:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
    #         detail='There was an error uploading the file')
    # finally:
    #     await file.close()
    # # print("filepath:")
    # # print(filepath)
    # dataDirectory = 'unzippedfiles/' + str(uuid)
    # if not os.path.exists("./unzippedfiles"):
    #     os.makedirs("./unzippedfiles")
    # import zipfile
    # with zipfile.ZipFile(filepath, 'r') as zip_ref:
    #     zip_ref.extractall(dataDirectory)
    # # # delete the zip file
    # # # os.remove(filepath)
    # print("BEFORE TASK")
    # task = divide.delay(1,2)
    images = await file.read()
    byte = base64.b64encode(images)
    data = {
            'image': byte.decode('utf-8'),
        }
    task = train.delay(data)
    return {"message": f"Successfuly uploaded "}



@celery.task#(serializer='pickle')
def train(data):
    print("IN TRAIN")
    print(data)
    import os
    outputFolder = "test-output-folder"
    dataDirectory = "unzippedfiles/f9b98410-8e37-469e-99f5-6dc6eb0b7105"
    # uuid = uuid4()
    # # check if directory "userzipfiles" exists, if not create it
    # if not os.path.exists("./userzipfiles"):
    #     os.makedirs("./userzipfiles")
    # try:
    #     print("abc")
    #     filepath = './userzipfiles/' + str(uuid) + '.zip'
    #     print(filepath)
    #     async with aiofiles.open(filepath, 'wb') as f:
    #         while chunk := await file.read(CHUNK_SIZE):
    #             await f.write(chunk)
    # except Exception:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
    #         detail='There was an error uploading the file')
    # finally:
    #     await file.close()
    # f = open('output.zip', 'wb')
    # # save file bytes to zip file
    # f.write(file)
    # f.close()
#     print("LHUILLIER STARTING TASK")
#     os.system(f"accelerate launch train_dreambooth.py \
#   --pretrained_model_name_or_path='CompVis/stable-diffusion-v1-4'  \
#   --instance_data_dir={dataDirectory} \
#   --output_dir={outputFolder} \
#   --instance_prompt='photo of sks dog' \
#   --resolution=512 \
#   --train_batch_size=1 \
#   --gradient_accumulation_steps=1 \
#   --learning_rate=5e-6 \
#   --lr_scheduler='constant' \
#   --lr_warmup_steps=0 \
#   --max_train_steps=800")

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