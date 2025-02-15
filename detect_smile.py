import cv2
from _datetime import datetime

face_classifier = cv2.CascadeClassifier('/Users/ccd/PycharmProjects/ComputerVision3/haarcascades/haarcascade_frontalface_default.xml')
smile_classifier = cv2.CascadeClassifier('/Users/ccd/PycharmProjects/ComputerVision3/haarcascades/haarcascade_smile.xml')

times = []
smile_ratios = []
cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        roi_gray = gray[y:y + h, x:x + w]
        roi_img = img[y:y + h, x:x + w]
        smile = smile_classifier.detectMultiScale(roi_gray, scaleFactor=1.2,
                                                  minNeighbors=22,
                                                  minSize=(25, 25))
        for (sx, sy, sw, sh) in smile:
            cv2.rectangle(roi_img, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 1)
            sm_ratio = str(round(sw / sx, 3))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Smile meter : ' + sm_ratio, (10, 50), font, 1, (200, 255, 155), 2, cv2.LINE_AA)
            if float(sm_ratio) > 1.8:
                smile_ratios.append(float(sm_ratio))
                times.append(datetime.now())
    cv2.imshow('Smile Detector', img)
    # Quit program
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
