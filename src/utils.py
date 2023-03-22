import pickle
import numpy as  np
import csv
import cv2

def show_npy_file(path, print=False):
    np_frame = np.load(path)
    
    if print == True:
        print(np_frame)

    cv2.imshow("npy frame", np_frame)
    cv2.waitKey(0)

def show_pkl_file(path,key=False):
    pkl = pickle.load(open(path, 'rb'))
    
    if key != False:
        print(pkl)
    else:
        print(pkl['{key}'])

# open multiple csv files and a make a single pickle file
def csvs_to_pkls(paths):
    for path in paths:
        accel = list(open(path, 'r'))