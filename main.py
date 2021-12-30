import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate, signal, optimize
from scipy.fftpack import fft, ifft, fftfreq, fftshift

from modules.signal_proccesing import SignalProcess
from modules.tracking_points import TrackingPoints
from modules.face_recon import Face

from modules.test_tracking import TrackPoints 


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
    tracking = TrackPoints(face, max_trace_history=300)
    #tracking = TrackingPoints(face, max_history_points_ = 300,max_points_=300)
    sig = SignalProcess(tracking, fps)
    print(f"Video FPS: {fps}")

    mean_bpm = []
    t = []
    mean_sys = []
    mean_dis = []
    while capture.isOpened():
        # Get a frame and wait for stable record
        ret, frame = capture.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = frame.copy()

        gray_frames.insert(0, gray)


        if frame_c >= 15:
            
            gray_frames.pop()
            tracking.track_points(gray_frames[1], gray_frames[0])
            longest_trace = max( [len(trace) for trace in tracking.traces] )

            # Find a longest trace 
            if longest_trace > 3*(fps):
                c_bpm, c_sist, c_dist = sig.find_bpm()
                if c_bpm != 0:
                    mean_bpm.append(c_bpm)
                    mean_sys.append(c_sist)
                    mean_dis.append(c_dist)
                    t.append(frame_c)
                if len(mean_bpm) != 0:
                    print(f"mean_BPM: {np.mean(mean_bpm)}, mean_sys: {np.mean(mean_sys)}, mean_dist: {np.mean(mean_dis)}")
            if cv2.waitKey(1) == 27: ## ESC
                break
        frame_c += 1

    plt.plot(t,mean_bpm)
    plt.show()
    print(np.mean(mean_bpm))
    capture.release()
    cv2.destroyAllWindows()

    print(args)

