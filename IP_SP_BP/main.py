import cv2
import numpy as np

from modules.face_recon import Face

from scipy import signal

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
    print(f"Video FPS: {fps}")
    face = Face()

    frame_c = 0

    Vr = []
    Vg = []
    Vb = []

    while(capture.isOpened()):
        ret, frame = capture.read()
        tmp = frame.copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2YCrCb)
        if frame is None:
            break

        points = face.get_roi_of_face(frame)

        face_roi = face.face_rectangle #[x1, y1, new_w, new_h]

        # if face.display == True:
        (Y, Cr, Cb) = cv2.split(tmp)

        gray_Y = cv2.bitwise_and(Y, Y, mask = cv2.cvtColor(face.mask, cv2.COLOR_BGR2GRAY))

        # cv2.imshow("Y channel", gray_Y)

        tmp = face.filterBySkinColor("Yellow", tmp)

        tmp = cv2.bitwise_and(tmp, tmp, mask = cv2.cvtColor(face.mask, cv2.COLOR_BGR2GRAY))

        #signal preprocessing

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


        # tmp_det = signal.detrend(V)

        # print(tmp_det)

        # w = 10 / (fps / 2)
        # a, b = signal.butter(5, w, 'highpass')

        # tmp_det = signal.filtfilt(a, b, tmp_det)

        # tmp_norm = (tmp_det - tmp_det.mean()) / tmp_det.std()

        


        # print(V)


        if type(points) == type(None):
            continue

        # cv2.imshow("Color convertion", tmp)

        if cv2.waitKey(1) == 27: ## ESC
            break
        frame_c += 1
        print(frame_c)

    #cv2.waitKey(0)

    print(Vr)
    print(Vg)
    print(Vb)

    capture.release()
    cv2.destroyAllWindows()