from logging import raiseExceptions
import cv2
import mediapipe as mp
from sklearn import metrics
from PIL import Image
from img2vec_pytorch import Img2Vec
import numpy as np
from flask import Flask, Response

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = []
img2vec = Img2Vec(cuda=False)
app = Flask(__name__)

def get_iou(bounding_box1, bounding_box2):

    x_left = max(bounding_box1['x1'], bounding_box2['x1'])
    y_top = max(bounding_box1['y1'], bounding_box2['y1'])
    x_right = min(bounding_box1['x2'], bounding_box2['x2'])
    y_bottom = min(bounding_box1['y2'], bounding_box2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    bounding_box1_area = (bounding_box1['x2'] - bounding_box1['x1']) * (bounding_box1['y2'] - bounding_box1['y1'])
    bounding_box2_area = (bounding_box2['x2'] - bounding_box2['x1']) * (bounding_box2['y2'] - bounding_box2['y1'])


    iou = intersection_area / float(bounding_box1_area + bounding_box2_area - intersection_area)

    return iou

def to_blur(target_face):
    try:
        target_face_img = Image.fromarray(target_face)
        target_embedding = img2vec.get_vec(target_face_img, tensor=True)
        for face_embedding in faces:
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.reshape((1, -1)), face_embedding.reshape((1, -1)))
            if validation_score > 0.5:
                return True
    except Exception as e:
        print("To blur exception: ", e)
    return False

def get_stream():

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("rtmp://192.168.162.218/live/pinnacle")

    counter = 0
    
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:

        last_blured_face_bbox = None
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
            
            # iterate over all faces
            bboxes = [ ]
            face_to_blur = None
            if results.detections:
                for detection in results.detections:
                    x = int(detection.location_data.relative_bounding_box.xmin * width_img)
                    y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                    width = int(detection.location_data.relative_bounding_box.width * width_img)
                    height = int(detection.location_data.relative_bounding_box.height * height_img)

                    cv2.rectangle(frame,(x,y),(x+width,y+height),(255,255,0),2)

                    bboxes.append((x, y, width, height))
                    
                    # if time to run embedding model
                    if counter == 0:
                        face = frame[y:y+height, x:x+width]
                        blur_face = to_blur(face)
                        if blur_face:
                            face_to_blur = (x, y, width, height)

            if counter != 0 and last_blured_face_bbox is not None:
                closest_bbox = None
                max_iou = 0
                xl,yl,wl,hl = last_blured_face_bbox
                last_bbox_as_dict = {"x1": xl, "y1": yl, "x2": xl+wl, "y2": yl+hl}
                for (x,y,w,h) in bboxes:
                    # compute IOU
                    curr_bbox_as_dict = {"x1": x, "y1": y, "x2": x+w, "y2": y+h}
                    curr_iou = get_iou(curr_bbox_as_dict, last_bbox_as_dict) 
                    if curr_iou > max_iou:
                        closest_bbox = (x,y,w,h)
                        max_iou = curr_iou
                print(f"best iou is {max_iou}")
                face_to_blur = closest_bbox
            elif counter !=0 and last_blured_face_bbox is None:
                print("last time we ran embedding model, there was no match. cannot interpolate")

            # blur face
            if face_to_blur is not None:
                x, y, width, height = face_to_blur
                try:
                    temp = cv2.resize(face, (5, 5), interpolation=cv2.INTER_LINEAR)
                    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                    frame[y:y+height, x:x+width] = output
                except Exception as e:
                    print("Exception: ", e)
                if counter == 0:
                    cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),2)
                    print("ran embedding model and similar face detected")
                else:
                    cv2.rectangle(frame,(x,y),(x+width,y+height),(255,0,0),2)
                    print("interpolated from preev embedding")
            elif face_to_blur is None and counter == 0:
                print("ran embedding model but no face is simlar")

            if counter == 0:
                last_blured_face_bbox = face_to_blur

            counter = (counter + 1) % 10

            # if counter == 0:
            #     last_detected_boxes = []
            #     last_blurred_bool = []
            #     last_detected_bounding_boxes = []
            # if results.detections:
            #     temp_set = set()
            #     for detection in results.detections:
                   
            #         x = int(detection.location_data.relative_bounding_box.xmin * width_img)
            #         y = int(detection.location_data.relative_bounding_box.ymin * height_img)
                    
            #         width = int(detection.location_data.relative_bounding_box.width * width_img)
            #         height = int(detection.location_data.relative_bounding_box.height * height_img)
            #         current_center = np.array([(x+width)/2, (y+height)/2])[None]
            #         face = frame[y:y+height, x:x+width]
            #         blur_face = None
            #         bounding_box_dict = {"x1": x, "y1": y, "x2": x+width, "y2": y+height}
            #         if counter == 0:
            #             blur_face = to_blur(face)
            #             last_detected_boxes.append(current_center)
            #             last_blurred_bool.append(blur_face)
            #             last_detected_bounding_boxes.append(bounding_box_dict)
            #         if blur_face is None:
            #             ious = [get_iou(temp,bounding_box_dict) for temp in last_detected_bounding_boxes]
            #             ious = np.array(ious)
            #             print("IOUS", ious)
            #             print(last_blurred_bool)
            #             if ious.any():
            #                 idx = (-ious).argsort()
            #                 if idx in temp_set:
            #                     raise RuntimeError
            #                 temp_set.add(idx)
                            
            #                 print(idx)
            #             else:
            #                 idx = (((last_detected_boxes - current_center)**2).sum(axis=1)).argmin()
            #             last_detected_boxes[idx] =(current_center)
            #             last_detected_bounding_boxes[idx] =(bounding_box_dict)
            #             print(len(last_blurred_bool), len(last_detected_boxes))
            #             print(idx)
            #             blur_face = last_blurred_bool[idx]
            #         if blur_face:
            #             print("Blur")
            #             w, h = (5, 5)
            #             if(type(face) == type(None)):
            #                 pass
            #             else:
            #                 try:
            #                     temp = cv2.resize(face, (w, h), interpolation=cv2.INTER_LINEAR)
            #                     output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
            #                     frame[y:y+height, x:x+width] = output
            #                 except Exception as e:
            #                     print("Failed to blur: ", e)
            #     if counter ==0:
            #         last_detected_boxes = np.concatenate(last_detected_boxes)

            #    cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),2)
                #counter = (counter + 1) % modulo

            cv2.imshow('Pinnacle', frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            og_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + og_frame + b'\r\n')
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
    print("We run here")

@app.route('/video_feed')
def video_feed():
    return Response(get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    main()
    app.run(debug=True)