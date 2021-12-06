import cv2 as cv
import numpy as np

class Face:

    def __init__(self):
        # Add predictor type, 
        # In first instance we'll be using  cv2.CascadeClassifier
        face_cascade_name = "./data/haarcascades/haarcascade_frontalface_alt.xml"
        eyes_cascade_name = "./data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"
        self.face_cascade = cv.CascadeClassifier()
        self.eyes_cascade = cv.CascadeClassifier()
        self.face_rectangle = [0,0,0,0]
        self.display = False
        self.params = dict(maxCorners = 500,
                        qualityLevel = 0.01,
                        minDistance = 3,
                        blockSize = 7 )
        if not self.face_cascade.load(cv.samples.findFile(face_cascade_name)):
            print("Error on loading cascade file name")
            exit(-1)
        if not self.eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
            print("Error on loading cascade eyes file name")
            exit(-1)

    def detect(self, gray_frame):
        gray_frame = cv.equalizeHist(gray_frame)
        faces_roi = self.face_cascade.detectMultiScale(gray_frame)
        face_sizes = [h * w for x,y,w,h in faces_roi]
        if self.display:
            for x,y,w,h in faces_roi:
                cv.rectangle(gray_frame, (x,y), (x+w, y+h), (0,255), 2)
            cv.imshow("Capture - face detection", gray_frame)
        # Get the bigger one
        return faces_roi

    def get_mask(self, gray_frame):
        mask = np.zeros(gray_frame.shape, np.uint8)
        if self.face_rectangle is not None:
            x,y,w,h = self.face_rectangle[0]
            mask[y:y+h, x:x+w] = 255
        if self.display:
            cv.imshow("Face mask", mask)
        self.mask = mask
        return mask

    def get_roi_of_face(self, gray_frame):
        self.face_rectangle = self.detect(gray_frame)
        self.get_mask(gray_frame)
        track_points = cv.goodFeaturesToTrack(gray_frame, mask=self.mask, **self.params)
        print("Track points:")
        print(track_points)
        return track_points


if __name__ == "__main__":
    face = Face()
    face.display = True
    cap = cv.VideoCapture("/tmp/test.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        tmp = frame.copy()
        if frame is None:
            break
        print(frame,ret)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        points = face.get_roi_of_face(gray)
#        if points is not None:
#            for i in points:
#                xc, yc = i.ravel()
#                cv.circle(tmp, (xc,yc), 3, 255, -1)
        cv.imshow("Final points", gray)
        #detectAndDisplay(gray, face)
        if cv.waitKey(1) == 27: ## ESC
            break


    cap.release()
    cv.destroyAllWindows()
