import os, subprocess

from sqlalchemy.orm import Session
from database import SessionLocal

def get_db(): 
    db: Session = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()


# Function to get the audio from a video 
def extract_audio(filename: str): 
    videos_dir = './videos/'
    audio_dir = './audio/'
    audio_filename = filename.split('.')[0] + '.mp3'

    # Make sure the video exists 
    if filename not in os.listdir(videos_dir): 
        raise ValueError(f'File {filename} does not exist in the videos directory')
    
    # Run the ffmpeg command 
    extract_audio_commands = ['ffmpeg', '-i', f'{videos_dir}{filename}', f'{audio_dir}{audio_filename}']
    if subprocess.call(extract_audio_commands) == 0: 
        print('Converted to audio successfully')
    else: 
        raise ValueError(f'Unable to convert video {videos_dir}{filename}')


# Get captions 
def get_captions(filename): 
    '''Extract captions from the mp3 file'''
    pass 

if __name__ == '__main__': 
    # Testing audio extraction
    extract_audio('sample_video.mp4')