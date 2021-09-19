import aiofiles
from fastapi import FastAPI, File, UploadFile

import models
from config import settings
from database import engine
from dependencies import get_db, get_captions, extract_audio, detect_code_words, contact_emergency_services

# Initialize the models 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def home(): 
    return  {'msg': 'This is the magic 4 pinnacle project'}


@app.post('/caption')
async def caption_video(uploaded_video: UploadFile = File(...)): 
    ''' Caption Endpoint
    To use this endpoint, send a video file as a form input. 

    '''
    print('Processing file: ', uploaded_video.filename)
    captions_dir = './captions'
    videos_dir = './videos'
    filename_without_extension = uploaded_video.filename.split('.')[0]
    captions_save_path = f'{captions_dir}/cap__{filename_without_extension}.txt'
    videos_save_path = f'{videos_dir}/up__{uploaded_video.filename}'


    # Get the file & save to the videos folder
    async with aiofiles.open(videos_save_path, 'wb') as out_file: 
        content = await uploaded_video.read()
        await out_file.write(content)

    # Extract audio
    extract_audio(f'up__{uploaded_video.filename}')
    audio_save_path = f'./audio/up__{filename_without_extension}.flac'
    # Get the captions & Save to file 
    captions = get_captions(audio_save_path)
    async with aiofiles.open(captions_save_path, 'w') as captions_file: 
        await captions_file.write(captions)

    # Detect code words 
    if detect_code_words(captions): 
        # Contact emergency services
        contact_emergency_services()
    

# TODO 1 register a user 

# TODO 2: Login a user 

