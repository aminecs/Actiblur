import io, os, subprocess

from sqlalchemy.orm import Session
from google.cloud import speech

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
    audio_filename = filename.split('.')[0] + '.flac'

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
    client = speech.SpeechClient()

    with io.open(filename, "rb") as audio_file:
        audio_file_content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=audio_file_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        enable_automatic_punctuation=True,
        language_code='en-US',
        audio_channel_count=2,
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == '__main__': 
    # Testing audio extraction
    # extract_audio('sample_video.mp4') # took like 11s 
    get_captions('./audio/sample_video.flac')