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