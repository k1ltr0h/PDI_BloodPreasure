import cv2 as cv
import numpy as np

class TrackingPoints:
    def __init__(self, face_detector_, max_points_ = 50):

        self.face_detector = face_detector_
        self.max_points = max_points_

    def getPoints(self, frame):
        points = self.face_detector.get_roi_of_face(frame)

        if points is None:
            return []

        return np.int32(points).reshape(-1, 2)


if __name__ == "__main__":

    from face_recon import Face

    cap = cv.VideoCapture(0)

    face_detector = Face("../data/haarcascades/haarcascade_frontalface_alt.xml",
                        "../data/haarcascades/haarcascade_eye_tree_eyeglasses.xml")
    tracker = TrackingPoints(face_detector_ = face_detector)

    while cap.isOpened():

        ret, frame = cap.read()

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        points = tracker.getPoints(gray_frame)

        for point in points:
            #print(point, tuple(point))
            frame = cv.circle(frame, tuple(point), 2, (255, 0, 255), -1)

        cv.imshow("Tracking", frame)

        if cv.waitKey(1) == 27: ## ESC
                break

    cap.release()
    cv.destroyAllWindows()



