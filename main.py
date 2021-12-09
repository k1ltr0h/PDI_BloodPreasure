import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate, signal, optimize
from scipy.fftpack import fft, ifft, fftfreq, fftshift

from modules.signal_proccesing import SignalProcess
from modules.tracking_points import TrackingPoints
from modules.face_recon import Face

from modules.tracking_points import TrackingPoints

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default=None, help = "Process a file instead of video recording")

    args = parser.parse_args()
    if args.file == None:
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture(args.file)

    fps = int(capture.get(cv2.CAP_PROP_FPS)) 

    gray_frames = []
    frame_c = 0
    face = Face()
    #tracking = TrackingPoints(face, max_points_=300)
    #tracking = TrackPoints(Face)
    tracking = TrackingPoints(face, max_history_points_ = 300)
    sig = SignalProcess(tracking, fps)
    print(f"Video FPS: {fps}")

    mean_bpm = []
    t = []
    while capture.isOpened():
        # Get a frame and wait for 15 frames to pass
        ret, frame = capture.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = frame.copy()

        #gray_frames.insert(0, gray)

#        points = tracking.getPoints(gray)
#        tracking.filter_points(points, gray)
#        prev_points = tracking.prev_points.reshape(-1, 2)


        #if frame_c >= 15:
            
        #gray_frames.pop()
        
        #points = tracking.getPoints(gray_frames)
        #tracking.filter_points(points, gray_frames)
        #prev_points = tracking.prev_points.reshape(-1, 2)
        #print(prev_points)

        points = tracking.getPoints(gray)
        tracking.filter_points(points, gray)

        longest_trace = max( [len(trace) for trace in tracking.history_points] )
        if longest_trace >= 2 * (fps + 1):
            bpm = sig.find_bpm()
            if bpm != 0:
                mean_bpm.append(bpm)
                t.append(frame_c)
            if len(mean_bpm) != 0:
                print(f"Len: {longest_trace} - BMP: {bpm} - mean_BPM: {sum(mean_bpm)/len(mean_bpm)}")
            #print(bpm)
            #print(mean_bpm)
        #points = face.get_roi_of_face(gray)
        if type(points) == type(None):
            continue
        points = np.int0(points)
        if points is not None:
            for i in points:
                x, y = i.ravel()
                cv2.circle(vis, (x,y),3,255,-1)
        cv2.imshow("Final points", vis)
        #detectAndDisplay(gray, face)
        if cv2.waitKey(1) == 27: ## ESC
            break
        frame_c += 1

    plt.plot(t,mean_bpm)
    plt.show()
    print(np.mean(mean_bpm))
    capture.release()
    cv2.destroyAllWindows()

    print(args)


'''
    capture = cv2.VideoCapture("./data/face_videos/p1.mp4")

    fps = int(capture.get(cv2.CAP_PROP_FPS))

    gray_frames = []  
    frame_c = 0

    face = FacePoints(dedector_type="haar")
    tracking = TrackPoints(face_dedector=face,max_trace_history=300)
    sig = SignalProcess(tracking,fps)
    mean_bpm=[]
    t=[]
 
    while capture.isOpened():
        # getting a frame
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = frame.copy()

        gray_frames.insert(0, gray)
   
        if frame_c >= 3:
            
            gray_frames.pop()
            tracking.track_points(gray_frames[1], gray_frames[0])
            longest_trace = max( [len(trace) for trace in tracking.traces] )
     
            if longest_trace >= 2*(fps+1):
                bpm=sig.find_bpm()
                mean_bpm.append(bpm)

                t.append(frame_c)
               
                

        if cv2.waitKey(1) == 27:
            break
        frame_c += 1

    plt.plot(t,mean_bpm)
    plt.show()
    print(np.mean(mean_bpm))
    capture.release()
    cv2.destroyAllWindows()
'''