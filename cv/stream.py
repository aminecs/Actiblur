import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def get_stream():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        while True:
            success, frame = cap.read()
            height_img, width_img, channels = frame.shape
            if not success:
                print("Ignoring empty camera frame.")
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
                    w, h = (5, 5)
                    if(type(face) == type(None)):
                        pass
                    else:
                        try:
                            temp = cv2.resize(face, (w, h), interpolation=cv2.INTER_LINEAR)
                            output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
                            frame[y:y+height, x:x+width] = output
                        except Exception as e:
                            print(e)
                    cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),2)
            cv2.imshow('Pinnacle', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()

get_stream()