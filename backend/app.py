from fastapi import FastAPI

from dependencies import get_db

app = FastAPI()


@app.get('/')
async def home(): 
    return  {'msg': 'This is the magic 4 pinnacle project'}