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
        for face_embedding in faces:
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
            if validation_score > 0.6:
                return True
    except Exception as e:
        print("To blur exception: ", e)
    return False

def read_video():

    cap = cv2.VideoCapture("demo.m4v")
    print(cap.isOpened())
    frames = []
    # while True:
    #     success, frame = cap.read()
    #     cv2.imshow('Pinnacle', frame)
    #     if cv2.waitKey(5) & 0xFF == 27:
    #         break
    # cap.release()
    # cv2.destroyAllWindows()
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
                        temp = cv2.resize(face, (5, 5), interpolation=cv2.INTER_LINEAR)
                        output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                        frame[y:y+height, x:x+width] = output
            #cv2.imshow('Frame',frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            frames.append(frame)
            print("Frame added")
            #print(frames)
        print("DONE")
        cap.release()
        cv2.destroyAllWindows()
        fourcc = cv2.VideoWriter_fourcc('a','v','c','1')
        writer = cv2.VideoWriter('blurred_no_tele.mp4',fourcc, 25.0, (frames[0].shape[1], frames[0].shape[0]))
        
        for i in range(0, len(frames)):
            writer.write(frames[i])
        writer.release()
    
def main():
    james = cv2.cvtColor(cv2.imread("James.jpg"), cv2.COLOR_BGR2RGB)
    janice = cv2.cvtColor(cv2.imread("Janice.jpg"), cv2.COLOR_BGR2RGB)
    tele = cv2.cvtColor(cv2.imread("Tele.jpg"), cv2.COLOR_BGR2RGB)
    friends = [james, janice]
    for friend in friends:
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
                        faces.append(embedding)

    read_video()
main()