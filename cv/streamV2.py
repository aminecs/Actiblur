import cv2
import mediapipe as mp
from sklearn import metrics
from PIL import Image
from img2vec_pytorch import Img2Vec
import time
from flask import Flask, Response


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = dict()
img2vec = Img2Vec(model="alexnet",cuda=False)
app = Flask(__name__)

def to_blur(target_face):
    try:
        target_face_img = Image.fromarray(target_face)
        target_embedding = img2vec.get_vec(target_face_img, tensor=True)
        for face_embedding_keys in faces.keys():
            face_embedding = faces[face_embedding_keys]
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
            print(validation_score)
            # Heuristically defined validation score
            if validation_score > 0.47:
                print(f"Good validation {validation_score} with {face_embedding_keys}")
                return True
    except Exception as e:
        print("To blur exception: ", e)
    return False

def get_stream():

    #cap = cv2.VideoCapture("rtmp://192.168.154.57/live/pinnacle")
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:

        while cap.isOpened():
            success, frame = cap.read()
            if type(frame) == type(None):
                break
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
                        try:
                            temp = cv2.resize(face, (5, 5), interpolation=cv2.INTER_LINEAR)
                            output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                            frame[y:y+height, x:x+width] = output
                        except Exception as e:
                            print(f"Exception {e}")

            #cv2.imshow('Frame',frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            og_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + og_frame + b'\r\n')
            if cv2.waitKey(5) & 0xFF == 27:
                break

    
def main():
    janice = cv2.cvtColor(cv2.imread("janiceV2.jpg"), cv2.COLOR_BGR2RGB)
    me = cv2.cvtColor(cv2.imread("me.jpeg"), cv2.COLOR_BGR2RGB)
    friends = [("Janice", janice), ("Amine", me)]
    for name, friend in friends:
        height_img, width_img, _ = friend.shape
        with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
                friend.flags.writeable = False
                results = face_detection.process(friend)

                friend.flags.writeable = True
                friend = cv2.cvtColor(friend, cv2.COLOR_RGB2BGR)
                if results.detections:
                    for detection in results.detections:
                        x = int(detection.location_data.relative_bounding_box.xmin * width_img)
                        y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                        width = int(detection.location_data.relative_bounding_box.width * width_img)
                        height = int(detection.location_data.relative_bounding_box.height * height_img)
                        face = friend[y:y+height, x:x+width]
                        face_img = Image.fromarray(face)
                        embedding = img2vec.get_vec(face_img, tensor=True)
                        faces[name] = embedding

@app.route('/video_feed')
def video_feed():
    return Response(get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    main()
    app.run(debug=True)