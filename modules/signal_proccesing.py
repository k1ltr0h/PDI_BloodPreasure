
import numpy as np
import cv2

import matplotlib.pyplot as plt

from scipy import interpolate, signal, optimize
from scipy.fftpack import fft, ifft, fftfreq, fftshift

from sklearn.decomposition import PCA


#from modules.face import FacePoints
from modules.face_recon import Face
from modules.tracking_points import TrackingPoints





class SignalProcess:

    def __init__(self, signal_source, fs=30):

        self.signal_source = signal_source
        self.fs = fs

        self.bpm_list = []
        self.mean_bpm = 0




    def get_y(self, traces):

        traces = [trace for trace in traces if len(trace) > 2*self.fs]
        trace_max_len = max( [len(trace) for trace in traces] )

        traces = [trace for trace in traces if len(trace) == trace_max_len]

        signal_y = []
        for trace in traces:
            trace = np.array(trace)[:, 1]

            signal_y.append(trace)
        return np.stack(signal_y, axis=0)

    def filter_butt(self, signal_data, fs=30, low_c=0.75, high_c=2.0):

        N = len(signal_data)

        T = 1.0 / fs

        #Dibuja la señal
        t = np.linspace(0.0, T*N, N)

        fc = np.array([low_c, high_c])
        #func de trans
        w = fc / (fs / 2) 
        b, a = signal.butter(5, w, 'bandpass')
        
        #filtrado
        filter_output = signal.filtfilt(b, a, signal_data)

        return filter_output

    def filter_signals(self, signals, low_c=0.5, high_c=2.0):
 
        filtered_signals = []

        for signal_data in signals:
            filter_out = self.filter_butt(signal_data, fs=self.fs, low_c=low_c, high_c=high_c)
            filtered_signals.append(filter_out)

        if len(filtered_signals) > 0:
            filtered_signals = np.stack(filtered_signals, axis=0)

        return filtered_signals[:-self.fs]


    def get_dominant_frequency(self, signal_data, fs=30):


        N = len(signal_data)
        T = 1.0 / fs
        
        spectrum = np.abs(fft(signal_data))
        spectrum *= spectrum
        xf = fftfreq(N, T)

        maxInd = np.argmax(spectrum)
        maxFreqPow = spectrum[maxInd]
        maxFreq = np.abs(xf[maxInd])

        total_power = np.sum(spectrum)
        percentage = maxFreqPow / total_power


        return maxFreq, percentage


    def pca(self, filtered_signals, fps):

        if len(filtered_signals) < 5:
            return 0

        pca = PCA(n_components=5)
        pca_result = pca.fit_transform(filtered_signals.T).T
        
        #Busca señal mas periodica
        max_ratios = []
        max_freqs = []
        for i, signal_data in enumerate(pca_result):
            maxFreq, percentage = self.get_dominant_frequency(signal_data, fs=fps)
            max_ratios.append(percentage)
            max_freqs.append(maxFreq)

        
        idx = np.argmax(max_ratios)
        last_pca = pca_result[idx]

        bpm = max_freqs[idx]*60

        return bpm

    def find_bpm(self, bpm_list_len=10, low_c=0.5, high_c=3.0):

        bpm = 0

        traces = self.get_y(self.signal_source.history_points)
        
        filtered_signals = self.filter_signals(traces, low_c=low_c, high_c=high_c)

        bpm = self.pca(filtered_signals, self.fs)

        self.bpm_list.insert(0, bpm)

        if len(self.bpm_list) > bpm_list_len:
            self.bpm_list.pop()

        self.mean_bpm = sum(self.bpm_list) / len(self.bpm_list)

        return bpm
    

if __name__ == "__main__":


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