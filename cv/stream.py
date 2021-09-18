import cv2
import mediapipe as mp
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn import metrics
from PIL import Image
from img2vec_pytorch import Img2Vec
import torch, torchvision
import numpy as np

resnet = InceptionResnetV1(pretrained='vggface2').eval()
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = []
img2vec = Img2Vec(cuda=False)

def to_blur(target_face):
    try:
        target_face_img = Image.fromarray(target_face)
        target_embedding = resnet(torchvision.transforms.ToTensor()(target_face_img).unsqueeze_(0))
        #target_embedding = resnet(target_face.unsqueeze(0))
        for face_embedding in faces:
            print(target_embedding.detach().numpy())
            print(face_embedding.detach().numpy())
            validation_score = metrics.pairwise.cosine_similarity(target_embedding.detach().numpy(), target_embedding.detach().numpy())
            print(validation_score)
            if validation_score > 0.6:
                return True
    except Exception as e:
        print(e)
    return False

def get_stream():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        while True:
            success, frame = cap.read()
            height_img, width_img, _ = frame.shape
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
                    if to_blur(face):
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
                    image_tensor = torchvision.transforms.ToTensor()(face_img).unsqueeze_(0)
                    #face2 = torchvision.transforms.functional.to_tensor(face).unsqueeze(0)
                    #embedding = resnet(torch.as_tensor(np.uint8(face)).unsqueeze(0).permute(0,3,1,2))
                    # face_temp = torch.transforms.functional.to_tensor(face)
                    
                    embedding = resnet(image_tensor)

                    #embedding = img2vec.get_vec(face_img, tensor=True)
                    faces.append(embedding)

    get_stream()

main()