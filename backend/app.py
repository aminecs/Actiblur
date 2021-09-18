from fastapi import FastAPI

import models
from database import engine
from dependencies import get_db

# Initialize the models 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def home(): 
    return  {'msg': 'This is the magic 4 pinnacle project'}