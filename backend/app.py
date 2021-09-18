from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def home(): 
    return  {'msg': 'This is the magic 4 pinnacle project'}