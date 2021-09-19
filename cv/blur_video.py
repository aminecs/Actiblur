import cv2
import mediapipe as mp
from sklearn import metrics
from PIL import Image
from img2vec_pytorch import Img2Vec
import time

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = []
img2vec = Img2Vec(cuda=False)

def to_blur(target_face):
    try:
        target_face_img = Image.fromarray(target_face)
        start = time.time()
        target_embedding = img2vec.get_vec(target_face_img, tensor=True)
        diff = time.time() - start
        for face_embedding in faces:
            start = time.time()
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
            diff = time.time() - start
            #print(diff)
            if validation_score > 0.5:
                return True
    except Exception as e:
        print("To blur exception: ", e)
    return False

def read_video():

    cap = cv2.VideoCapture(0)
    frames = []
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:

        while cap.isOpened():
            success, frame = cap.read()
            height_img, width_img, _ = frame.shape

            if not success:
                print("Frame not found")
                continue
        
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            results = face_detection.process(frame)

            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if results.detections:
                for detection in results.detections:
                    x = int(detection.location_data.relative_bounding_box.xmin * width_img)
                    y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                    width = int(detection.location_data.relative_bounding_box.width * width_img)
                    height = int(detection.location_data.relative_bounding_box.height * height_img)


                    face = frame[y:y+height, x:x+width]
                    cv2.rectangle(frame,(x,y),(x+width,y+height),(255,255,0),2)
                    blur_face = to_blur(face)
                    if blur_face:
                        face_to_blur = (x, y, width, height)
                    
                    temp = cv2.resize(face, (5, 5), interpolation=cv2.INTER_LINEAR)
                    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                    frame[y:y+height, x:x+width] = output
            
            frames.append(frame)
        fourcc = cv2.VideoWriter_fourcc('a','v','c','1')
        writer = cv2.VideoWriter('blurred.mp4',fourcc, 25.0, (frame.shape[1], frame.shape[0]))
        
        for i in range(0, len(frames)):
            writer.write(frames[i])
        writer.release()
    

read_video()