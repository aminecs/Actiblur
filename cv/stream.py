import cv2


def get_feed():
    cap = cv2.VideoCapture(0)


    while(True):
        ret, frame = cap.read()

        cv2.imshow('Pinnacle',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

get_feed()