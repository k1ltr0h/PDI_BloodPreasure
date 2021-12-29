import cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import FastICA
from modules.face_recon import Face

from scipy import signal

import argparse

# highpass filter

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
    
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default=None, help = "Process a file instead of video recording")

    args = parser.parse_args()
    if args.file == None:
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture(args.file)

    fps = int(capture.get(cv2.CAP_PROP_FPS)) 
    print(f"Video FPS: {fps}")
    assert(fps >= 20)
    face = Face()

    frame_count = 0

    Vr = []
    Vg = []
    Vb = []

    while(capture.isOpened()):
        ret, frame = capture.read()
        if not ret: 
            break

        if frame_count == 30*fps:
            break
        tmp = frame.copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2YCrCb)

        points = face.get_roi_of_face(frame)

        face_roi = face.face_rectangle #[x1, y1, new_w, new_h]

        tmp = face.filterBySkinColor("Yellow", tmp)

        tmp = cv2.bitwise_and(tmp, tmp, mask = cv2.cvtColor(face.mask, cv2.COLOR_BGR2GRAY))

        # signal preprocessing
        # frame in rgb
        tmp_rgb = cv2.cvtColor(tmp, cv2.COLOR_YCrCb2BGR)

        # get average per channel
        roi_size = face_roi[0][2] * face_roi[0][3]

        (B, G, R) = cv2.split(tmp_rgb)

        Vr_val = (1000 / roi_size)*np.sum(R)
        Vg_val = (1000 / roi_size)*np.sum(G)
        Vb_val = (1000 / roi_size)*np.sum(B)
        
        Vr.append(Vr_val)
        Vg.append(Vg_val)
        Vb.append(Vb_val)

        # print(V)

        if type(points) == type(None):
            continue

        # cv2.imshow("Color convertion", tmp)

        if cv2.waitKey(1) == 27: ## ESC
            break
        
        frame_count += 1
        if(frame_count%fps==0):
            print(str(int(frame_count/fps)) + "[s]")


    # signal preprocessing

    # detrending

    Vr_det = signal.detrend(Vr)
    Vg_det = signal.detrend(Vg)
    Vb_det = signal.detrend(Vb)

    Vr_filt = butter_highpass_filter(Vr_det,10,fps)
    Vg_filt = butter_highpass_filter(Vg_det,10,fps)
    Vb_filt = butter_highpass_filter(Vb_det,10,fps)

    # normalizing

    Vr_norm = (Vr_filt - Vr_filt.mean()) / Vr_filt.std()
    Vg_norm = (Vg_filt - Vg_filt.mean()) / Vg_filt.std()
    Vb_norm = (Vb_filt - Vb_filt.mean()) / Vb_filt.std()

    # print(Vb_norm)

    #ICA
    trial=Vg_norm.reshape(-1,1)
    ica = FastICA(n_components=1)
    Vg_ica = ica.fit_transform(trial)
    Vg_ica_def=[]
    for i in range(len(Vg_ica)):
        Vg_ica_def.append(Vg_ica[i][0])
    Vg_ica_def=np.asarray(Vg_ica_def)   
    
    #Peak-Detection
    peaks_up, _= signal.find_peaks(Vg_ica_def, height=0)
    peaks_down, _= signal.find_peaks(-Vg_ica_def, height=0) 
    
    #Plotting
#    plt.plot(Vg_ica[0:50])
#    plt.plot(peaks_up[0:50], Vg_ica_def[peaks_up][0:50], "x")
#    plt.plot(peaks_down[0:50], Vg_ica_def[peaks_down][0:50], "o")

    #Estimate BP
    Ep=[]
    for i in range(len(peaks_up)):
        Ep.append(Vg_ica_def[peaks_up[i]])
    
    Ev=[]
    for j in range(len(peaks_down)):
        Ev.append(Vg_ica_def[peaks_down[j]])
    Ep_mean=sum(Ep)/len(Ep)
    Ev_mean=sum(Ev)/len(Ev)
    bmi = 35.7
    SBP = 23.7889 + 95.4335 * Ep_mean + 4.5958 * bmi - 5.109 *Ep_mean*bmi
    DBP = -17.3772 - 115.1747 * Ev_mean + 4.0251 * bmi + 5.2825 * Ev_mean * bmi

    print("SBP: " + str(SBP) + "\tDBP: " + str(DBP))
    capture.release()
    cv2.destroyAllWindows()