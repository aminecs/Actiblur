import cv2
import mediapipe as mp
from sklearn import metrics
from PIL import Image
from img2vec_pytorch import Img2Vec
import threading, queue, time
import numpy as np

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = []
img2vec = Img2Vec(cuda=False)

# def to_blur(target_face):
#     try:
#         target_face_img = Image.fromarray(target_face)
#         start = time.time()
#         target_embedding = img2vec.get_vec(target_face_img, tensor=True)
#         diff = time.time() - start
#         print(diff)
#         for face_embedding in faces:
#             start = time.time()
#             validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
#             diff = time.time() - start
#             print(diff)
#             if validation_score > 0.8:
#                 return True
#     except Exception as e:
#         print("To blur exception: ", e)
#     return False

def to_blur(target_face):
    try:
        target_face_img = Image.fromarray(target_face)
        start = time.time()
        target_embedding = img2vec.get_vec(target_face_img, tensor=True)
        diff = time.time() - start
        #print(diff)
        for face_embedding in faces:
            start = time.time()
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
            diff = time.time() - start
            #print(diff)
            print(validation_score)
            if validation_score > 0.6:
                return True
    except Exception as e:
        print("To blur exception: ", e)
    return False

class Worker(threading.Thread):
    def __init__(self, q, output_q):
        self.q = q
        self.output_q = output_q
        super().__init__()
    def run(self):
        while True:
            self.get_prediction(self.q.get())
            self.q.task_done()
            
    def get_prediction(self, frame):
        res = to_blur(frame)
        if not res:
            self.output_q.put_nowait(False)
            return False
        else:
            self.output_q.put_nowait(res)
            return True

def get_stream():

    threaded = 0
    q = queue.Queue()
    output_q = queue.Queue()
    
    t = Worker(q, output_q)
    t.start()


    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("rtmp://192.168.162.218/live/pinnacle")

    counter = 0
    modulo = 30
    
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        while True:
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
            if counter == 0:
                last_detected_boxes = []
                last_blurred_bool = []
            if results.detections:
                for detection in results.detections:
                   
                    x = int(detection.location_data.relative_bounding_box.xmin * width_img)
                    y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                    
                    width = int(detection.location_data.relative_bounding_box.width * width_img)
                    height = int(detection.location_data.relative_bounding_box.height * height_img)
                    current_center = np.array([(x+height)/2, (y+width)/2])[None]
                    face = frame[y:y+height, x:x+width]
                    blur_face = None
                    if counter == 0:
                        blur_face = to_blur(face)
                        last_detected_boxes.append(current_center)
                        last_blurred_bool.append(blur_face)
                    if blur_face is None:
                        idx = (((last_detected_boxes - current_center)**2).sum(axis=1)).argmin()
                        print(len(last_blurred_bool), len(last_detected_boxes))
                        print(idx)
                        blur_face = last_blurred_bool[idx]
                    if blur_face:
                        print("Blur")
                        w, h = (5, 5)
                        if(type(face) == type(None)):
                            pass
                        else:
                            try:
                                temp = cv2.resize(face, (w, h), interpolation=cv2.INTER_LINEAR)
                                output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                                frame[y:y+height, x:x+width] = output
                            except Exception as e:
                                print("Failed to blur: ", e)
                if counter ==0:
                    last_detected_boxes = np.concatenate(last_detected_boxes)

                    # if not output_q.empty():
                    #     blur = output_q.get()

                    #     if blur:
                    #         w, h = (5, 5)
                    #         if(type(face) == type(None)):
                    #             pass
                    #         else:
                    #             try:
                    #                 temp = cv2.resize(face, (w, h), interpolation=cv2.INTER_LINEAR)
                    #                 output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                    #                 frame[y:y+height, x:x+width] = output
                    #             except Exception as e:
                    #                 print("Failed to blur: ", e)
                    
                    #     q.put_nowait(face)
                    # elif not threaded:
                    #     print("Here")
                    #     threaded = 1
                    #     q.put_nowait(face)
                cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),2)
                counter = (counter + 1) % modulo

            cv2.imshow('Pinnacle', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

def main():
    example_img = cv2.cvtColor(cv2.imread("me.jpeg"), cv2.COLOR_BGR2RGB)
    height_img, width_img, _ = example_img.shape
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
            example_img = cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB)
            example_img.flags.writeable = False
            results = face_detection.process(example_img)

            example_img.flags.writeable = True
            example_img = cv2.cvtColor(example_img, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    x = int(detection.location_data.relative_bounding_box.xmin * width_img)
                    y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                    width = int(detection.location_data.relative_bounding_box.width * width_img)
                    height = int(detection.location_data.relative_bounding_box.height * height_img)
                    face = example_img[y:y+height, x:x+width]
                    face_img = Image.fromarray(face)
                    embedding = img2vec.get_vec(face_img, tensor=True)
                    faces.append(embedding)

    get_stream()

main()