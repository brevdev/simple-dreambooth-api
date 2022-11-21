from celery import Celery
from fastapi import FastAPI

app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

@celery.task
def train():
    import time
    import os
    print("LHUILLIER STARTING TASK")
    time.sleep(5)
    os.system("sh launch-copy.sh")