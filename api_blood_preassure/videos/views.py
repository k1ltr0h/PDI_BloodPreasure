from rest_framework.response import Response
from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.views import APIView
import cv2
from modules.face_recon import Face
from modules.tracking_points import TrackingPoints
from modules.test_tracking import TrackPoints
from modules.signal_proccesing import SignalProcess
import numpy as np
# Create your views here.


def calculate_bpm(video):

    capture = cv2.VideoCapture(video)
    
    fps = int(capture.get(cv2.CAP_PROP_FPS)) 

    gray_frames = []
    frame_c = 0
    face = Face()
    #tracking = TrackingPoints(face, max_points_=300)
    tracking = TrackPoints(face, max_trace_history=300)
    #tracking = TrackingPoints(face, max_history_points_ = 300,max_points_=300)
    sig = SignalProcess(tracking, fps)
    
    mean_bpm = []
    t = []
    mean_sys = []
    mean_dis = []
    while capture.isOpened():
        # Get a frame and wait for 15 frames to pass
        ret, frame = capture.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = frame.copy()

        gray_frames.insert(0, gray)

#        points = tracking.getPoints(gray)
#        tracking.filter_points(points, gray)
#        prev_points = tracking.prev_points.reshape(-1, 2)


        if frame_c >= 15:
            
            gray_frames.pop()
        #points = tracking.getPoints(gray_frames)
        #tracking.filter_points(points, gray_frames)
        #prev_points = tracking.prev_points.reshape(-1, 2)
        #print(prev_points)

            #points = tracking.getPoints(gray)
            #tracking.filter_points(points, gray)
            #longest_trace = max( [len(trace) for trace in tracking.history_points] )
            tracking.track_points(gray_frames[1], gray_frames[0])
            longest_trace = max( [len(trace) for trace in tracking.traces] )

            
            #if longest_trace >= 2* (fps+1):
            if longest_trace > 3*(fps):
                c_bpm, c_sist, c_dist = sig.find_bpm()
                #bpm = sig.find_bpm()
                if c_bpm != 0:
                    mean_bpm.append(c_bpm)
                    mean_sys.append(c_sist)
                    mean_dis.append(c_dist)
                    t.append(frame_c)
                if len(mean_bpm) != 0:
                    print(f"mean_BPM: {np.mean(mean_bpm)}, mean_sys: {np.mean(mean_sys)}, mean_dist: {np.mean(mean_dis)}")
            #points = face.get_roi_of_face(gray)
            #if type(points) == type(None):
            #    continue
            #points = np.int0(points)
            #if points is not None:
            #    for i in points:
            #        x, y = i.ravel()
            #        cv2.circle(vis, (x,y),3,255,-1)
            #cv2.imshow("Final points", vis)
            #detectAndDisplay(gray, face)
            #if cv2.waitKey(1) == 27: ## ESC
                #break
        frame_c += 1
        if frame_c >= fps * 13:
            break


    return (np.mean(mean_bpm), np.mean(mean_sys), np.mean(mean_dis))



class Upload(APIView):
    def post(self, request):
        file = request.FILES['video']
        name = 'data_output/'+file.name
        file_name = default_storage.save(name, file)

        try:    
            bpm,sys,dis = calculate_bpm(name)
            return Response({'status': 'success',
                            'BPM':bpm,
                            'DIA': sys,
                            'SYS': dis,
                            })
        except:
            return Response({"status": "error",
                            'BPM':0,
                            'DIA': 0,
                            'SYS': 0,
                            })