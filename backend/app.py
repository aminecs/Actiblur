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

# TODO 1 register a user 

# TODO 2: Login a user 

# TODO 3: Take a video & generate captions 

# TODO 4: Detect safe word in caption/video 

# TODO 5: Make an emergency call with precise location data 