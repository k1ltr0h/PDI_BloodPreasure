import cv2 as cv
import numpy as np


## Referencias
# https://www.geeksforgeeks.org/python-opencv-optical-flow-with-lucas-kanade-method/
# https://docs.opencv.org/3.4/dc/d6b/group__video__track.html#ga473e4b886d0bcc6b65831eb88ed93323
# https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
# https://stackoverflow.com/questions/34540181/opencv-optical-flow-assertion


class TrackingPoints:
    def __init__(self, face_detector_, max_points_ = 100):

        self.face_detector = face_detector_
        self.traces = []
        self.max_points = max_points_
        self.prev_frame = None
        self.prev_points = []
        self.params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    def getPoints(self, frame):
        try:
            points = self.face_detector.get_roi_of_face(frame).reshape(-1, 2)
            #print(self.face_detector.get_roi_of_face(frame).shape)
        except:
            return []

        if points is None:
            return []

        #print(points[0])
        self.prev_points = self.traces
        self.traces = []
        for i in range(self.max_points):
            self.traces.append(points[i])

        return np.int32(self.traces).reshape(-1, 1, 2)

    def filter_points(self, points, frame):
        if len(points) < 1:
            return []

        if self.prev_frame is None or self.prev_points == []:
            self.prev_frame = frame
            self.prev_points = points
            #print("o.o\n")
            return points.reshape(-1, 2)
        
        #Forward optical flow
        next_points, st, err = cv.calcOpticalFlowPyrLK(self.prev_frame, frame, np.float32(points), None, **self.params)
        # Backward optical flow
        back_next_points, _st, _err = cv.calcOpticalFlowPyrLK(frame, self.prev_frame, next_points, None, **self.params) 
        
        # Find differance between 2 estimates
        # TODO: get distance
        #print(len(points), len(backNextPts))
        dist = abs(points-back_next_points).reshape(-1, 2).max(-1)

       # print(abs(points-backNextPts).reshape(-1, 2), abs(points-backNextPts).reshape(-1, 2).max(-1))

        # Select backtraced points that are in 1 pixel dist
        print(dist)
        filter = dist > 1

        print(len(points), len(filter))

        self.prev_frame = frame
        self.prev_points = points

        if next_points is None or next_points == []:
            self.track_started = False
            return

        next_points = next_points.reshape(-1, 2)

        # Reset tracking
        if len(next_points) < 1:
            self.track_started = False
            return

        #for i in next_points:
        #    print(i)

        # add from starting point
        new_traces = []
        for index_point in range(len(next_points)):
            # Delete unbacktrackable traces
            if filter[index_point]:
                continue
            self.traces[index_point] = next_points[index_point]

        # Add new traces if it shrink
        for point in points:
            if len(self.traces) < self.max_points:
                if point not in self.traces:
                    self.traces.append(point)
            else:
                break
            

        #print(len(points.reshape(-1, 2)), len(abs(points-backNextPts).reshape(-1, 2).max(-1)))
        #print(np.int32(next_points))
        
        return np.int32(next_points).reshape(-1, 2)


if __name__ == "__main__":

    from face_recon import Face

    cap = cv.VideoCapture(0)

    face_detector = Face("../data/haarcascades/haarcascade_frontalface_alt.xml",
                        "../data/haarcascades/haarcascade_eye_tree_eyeglasses.xml")
    tracker = TrackingPoints(face_detector_ = face_detector)

    while cap.isOpened():

        ret, frame = cap.read()

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if tracker.prev_frame is None:
            tracker.prev_frame = frame
            continue

        points = tracker.getPoints(gray_frame)
        #print(points)
        points = tracker.filter_points(points, gray_frame)

        prev_points = tracker.prev_points.reshape(-1, 2)

        for i, point in enumerate(points):
            #print(point, tuple(point))
            #print(tracker.prev_points)
            cv.line(frame, point, prev_points[i], (0, 0, 255), 2)
            frame = cv.circle(frame, tuple(point), 2, (255, 255, 0), -1)

        traces = np.int32(tracker.traces).reshape(-1, 1, 2)


        cv.imshow("Tracking", frame)

        if cv.waitKey(1) == 27: ## ESC
                break

    cap.release()
    cv.destroyAllWindows()



