import cv2 as cv
import numpy as np

class Face:

  def __init__(self, 
              face_cascade_name_ = "../data/haarcascades/haarcascade_frontalface_alt.xml",
              eyes_cascade_name_ = "../data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"):
      # Add predictor type, 
      # In first instance we'll be using  cv2.CascadeClassifier
      face_cascade_name = face_cascade_name_
      eyes_cascade_name = eyes_cascade_name_
      self.face_cascade = cv.CascadeClassifier()
      self.eyes_cascade = cv.CascadeClassifier()
      self.face_rectangle = [0,0,0,0]
      self.rois4calibrate = 20
      self.mask = []
      self.rois = []
      self.w_mean = 0
      self.h_mean = 0
      self.readjustment = 0.75
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

  def detect(self, frame):       
      faces_roi = self.face_cascade.detectMultiScale(frame)

      if len(self.rois) < self.rois4calibrate and faces_roi != ():
          # print("faces_roi: ", faces_roi)
          self.rois.append(faces_roi)
          
      if self.w_mean == 0 and self.h_mean == 0 and len(self.rois) == self.rois4calibrate:
          for roi in self.rois:
              x, y, w, h = roi[0]
              self.w_mean += w
              self.h_mean += h

          self.w_mean = int((self.w_mean/self.rois4calibrate)*self.readjustment)
          self.h_mean = int((self.h_mean/self.rois4calibrate)*self.readjustment)

          self.display = True

      #if self.display:
      counter = 0
      for x,y,w,h in faces_roi:
          x1, y1, x2, y2 = x, y, x + w, y + h

          if len(self.rois) >= self.rois4calibrate:
              w_var = w - self.w_mean
              h_var = h - self.h_mean

              if self.w_mean < w:
                  x1 = int(x1 + (w_var/2))
                  x2 = int(x2 - (w_var/2))

              if self.h_mean < h:
                  y1 = int(y1 + (h_var/2))
                  y2 = int(y2 - (h_var/2))

              if x1 - x2 != self.w_mean:
                  x2 = x2 + (self.w_mean - (x2 - x1))
              if y1 - y2 != self.h_mean:
                  y2 = y2 + (self.h_mean - (y2 - y1))
              #print(x1, y1, x2, y2)
              new_w = (x2-x1)
              new_h = (y2-y1)
              # print("w*h: ", new_w*new_h)

              faces_roi[counter] = [x1, y1, new_w, new_h]

          cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255), 2)
          counter += 1

      # cv.imshow("Capture - face detection", frame)
      # Get the bigger one
      return faces_roi

  def get_mask(self, frame):
      mask = np.zeros(frame.shape, np.uint8)
      if self.face_rectangle is not None and self.face_rectangle != ():
          x,y,w,h = self.face_rectangle[0]
          mask[y:y+h, x:x+w] = 255
      #if self.display:
      # cv.imshow("Face mask", mask)
      self.mask = mask
      return mask

  def get_roi_of_face(self, frame):
      self.face_rectangle = self.detect(frame)
      self.mask = self.get_mask(frame)
      return frame

  def filterBySkinColor(self, skin_color, YCrCbFrame):
      # shape prints the tuple (height,weight,channels)
      # print(YCrCbFrame.shape)
      if skin_color.lower() == "yellow":
          for row in range(YCrCbFrame.shape[0]):

          # get the pixel values by iterating
              for col in range(YCrCbFrame.shape[1]):
                  #print(YCrCbFrame[row][col])
                  for ch in range(YCrCbFrame.shape[2]):
                      value = YCrCbFrame[row][col][ch]

                      if ch == 1 and value < 170 and value > 120:
                          YCrCbFrame[row][col][ch] = 255
                      else:
                          YCrCbFrame[row][col][ch] = 0

                      if ch == 2 and value < 150 and value > 100:
                          YCrCbFrame[row][col][ch] = 255
                      else:
                          YCrCbFrame[row][col][ch] = 0

      # display image
      # cv.imshow("output", YCrCbFrame)

      return YCrCbFrame


  @staticmethod
  def point_in_rectangle(xx,yy, x, y, w, h):
      if xx >= x and xx <= x+w:
          if yy >= y and yy <= y+h:
              return True
      
      return False
