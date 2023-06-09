import sys
import os
import numpy as np
import argparse
import cv2
import pickle
import glob

# idea: generate all data in CSV and pickle format using just .mp4 and .csv data from OpenCamera Android app.
class DataLoader:
    def __init__(self, file_name, s_img=False, print_pkl=False):
        if file_name is None:
            raise Exception('No file name given')
        else:
            self.file_name = file_name
            self.dict_imu = None
            self.dict_frame_metadata = None
            self.dict_templates_live = None
            self.dict_intrinsics = None
            self.s_img = s_img
            self.print_pkl = print_pkl
            self.img_data_path = 'data/record/images'
            
            # 2 temp vars: for accel and gyro ts
            self.accel_ts = None
            self.gyro_ts = None
        
            try:
                # self.start_time = os.path.getctime(f'data/{self.file_name}.mp4')
                # self.start_time = 1679040345.0
                self.start_time = self.cap_time_data() # testing with original frame ts : opencamera format
                
            except ImportError:
                raise Exception('No creation time found.')
            
            cap = cv2.VideoCapture(f'data/{self.file_name}.mp4')
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            self.resolution = (width, height)
            print(f'Resolution := {self.resolution}')

    def reset_img_data(self):

        # TODO: Make sure it only deletes .npy files and not .gitkeep
        files = [f for f in os.listdir(self.img_data_path) if f != '.gitkeep']
        for file in files:
            file_path = os.path.join(self.img_data_path, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    # print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    def load_mp4_and_dump_npy(self):
        # import mp4 file
        cap = cv2.VideoCapture(f'data/{self.file_name}.mp4')
        fps = cap.get(cv2.CAP_PROP_FPS)

        nframe = 0
        meta_data = []

        self.reset_img_data()  # Clears all npy images in the data/record/images dir

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame to 848 x 480 px
            # frame = cv2.resize(frame, (848, 480))
            
            # convert RGB img to Grayscale
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)  # testing effect of blur
            else:
                break

            if self.s_img is True:
                cv2.imshow('frame', gray_frame)

            frame_array = np.array(gray_frame)

            np.save(open(f'data/record/images/frame_{nframe:06d}.npy', 'wb'), frame_array)

            nframe += 1

            # Get the current frame number and calculate the timestamp
            frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
            timestamp = self.start_time + (frame_num / fps)

            # Write the frame number and timestamp to the array
            meta_data.append(timestamp)

            # Wait for the user to press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f'Total frames = {nframe}')
        cap.release()
        cv2.destroyAllWindows()

        meta_data = np.array(meta_data)
        
        # Commenting to test new time cap
        # self.dict_frame_metadata = {
        #     'ts': meta_data
        # }
        
    def cap_time_data(self):
        
        # all ts in ns : need to convert to s
        accelT = np.genfromtxt(f'data/{self.file_name}accel.csv', delimiter=',')
        gyroT = np.genfromtxt(f'data/{self.file_name}gyro.csv', delimiter=',')
        frameT = np.genfromtxt(f'data/{self.file_name}imu_timestamps.csv', delimiter=',')
        
        start_time = np.min([accelT[0][-1], gyroT[0][-1], frameT[0]])
        
        meta_data = frameT/1e9 # convert from ns to s
        
        self.dict_frame_metadata = {
            'ts': meta_data
        }
        
        self.accel_ts = accelT[:, -1] / 1e9
        self.gyro_ts = gyroT[:, -1] / 1e9
                
        return start_time / 1e9

    def load_csv_files(self):

        # TODO: align axis of realsense imu and s23 camera imu - find axis x,y,z format of each

        # permutation matrix: changing z to negative
        perm = np.array([[0.0, -1.0, 0], [-1.0, 0.0, 0], [0, 0, -1.0]], dtype=float)

        data = np.genfromtxt(f'data/{self.file_name}accel.csv', delimiter=',')
        accel_data = data[:, :-1]

        # transform Open camera to Realsense axis
        accel_data = accel_data @ perm

        data = np.genfromtxt(f'data/{self.file_name}gyro.csv', delimiter=',')
        # print(data)
        gyro_data = data[:, :-1]
        
        gyro_data = gyro_data @ perm # testing switch of rows
        # print(gyro_data)


        # create a new column with timeseries of imu data TODO: Replace this
        # time_series_accel = np.linspace(self.start_time, self.dict_frame_metadata['ts'][-1], len(accel_data))
        # time_series_gyro = np.linspace(self.start_time, self.dict_frame_metadata['ts'][-1], len(gyro_data))

        # Testing with original time series
        time_series_accel = self.accel_ts
        time_series_gyro = self.gyro_ts
        # print(f'shape of a ts = {np.shape(time_series_accel)}')
        # print(f'shape of a data = {np.shape(accel_data)}')
        
        # tesinng with reshape
        accel_data = np.hstack((time_series_accel.reshape(-1,1), accel_data))
        gyro_data = np.hstack((time_series_gyro.reshape(-1,1), gyro_data))

        imu_data = {
            'accel': accel_data, 'gyro': gyro_data
        }
        self.dict_imu = imu_data

    def create_patches(self):
        
        start_time = self.start_time + 0.5
        end_time = self.start_time + 10000.0
        
        # patch_cords = (349+15, 165+15, 499-15, 315-15)
        patch_cords = (
            int(self.resolution[0]/2 - self.resolution[0] * 0.1),
            int(self.resolution[1]/2 - self.resolution[1] * 0.15),
            int(self.resolution[0]/2 + self.resolution[0] * 0.1),
            int(self.resolution[1]/2 + self.resolution[1] * 0.15)
        )
        # print(patch_cords)

        patches0 = (start_time, end_time, patch_cords)
        patches1 = (start_time+2.0, end_time, patch_cords)
        patches2 = (start_time+4.0, end_time, patch_cords)
        patches3 = (start_time+6.0, end_time, patch_cords)
        
        print(patches0)

        dict_templates_live = {
            'patches': [patches0]
        }

        self.dict_templates_live = dict_templates_live

    def load_intrinsics(self):
        D = np.array([0., 0., 0., 0.])
        resolution = self.resolution
        try:
            K = pickle.load(open('calibrate_imgs/intrinsics/cameraMatrix.pkl', 'rb'))
        except ImportError:
            raise Exception("no cameraMatrix.pkl found")
        else:
            intrinsics = {
                'K': K,
                'D': D,
                'resolution': resolution
            }
            # print(intrinsics)
            self.dict_intrinsics = intrinsics

    def dump_pickles(self):
        pickle.dump(self.dict_imu, open("data/record/imu.pickle", "wb"))
        pickle.dump(self.dict_frame_metadata, open("data/record/frame_metadata.pickle", "wb"))
        pickle.dump(self.dict_templates_live, open("data/record/templates_live.pickle", "wb"))
        pickle.dump(self.dict_intrinsics, open("data/record/intrinsics.pickle", "wb"))

        if self.print_pkl is True:
            print("===INTRINSICS==")
            print(self.dict_intrinsics)

            print("===FRAME-TIMESTAMPS==")
            print(self.dict_frame_metadata)

            print("===PATCH-TIMES==")
            print(self.dict_templates_live)

            print("===IMU==")
            print(self.dict_imu)

    # input -> output : file_name -> imu, frame_metadata, templates_live, npy dump
    def dump_files(self):
        self.load_mp4_and_dump_npy()
        self.load_csv_files()  # load fixed imu data
        self.create_patches()  # create a patch
        self.load_intrinsics()  # load intrinsics from calibration file
        self.dump_pickles()


if __name__ == '__main__':

    # parser name
    parser = argparse.ArgumentParser(description='Description of your program')

    # arguments
    parser.add_argument('-f', '--file', type=str, help='name of input file')
    parser.add_argument('-I', '--imshow', dest='imshow', action='store_true', help='Hide Imshow')
    parser.add_argument('-P', '--printpkl', dest='print_pkl', action='store_true', help='print all pickles')

    # parsing with error cases
    try:
        args = parser.parse_args()
    except NameError:
        print("Error in parsing file name")
        sys.exit(1)
    else:
        # check number of args
        if len(vars(args)) < 1:
            parser.error('Invalid number of arguments.')
        else:
            # get file name
            file_id = args.file

            # run function to import csv data
            print(f'file id := {file_id}')
            dataLoader = DataLoader(file_id, args.imshow, args.print_pkl)
            dataLoader.dump_files()