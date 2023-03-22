import sys
import os
import numpy as np
import argparse
import cv2
import pickle


# idea: generate all data in CSV and pickle format using just .mp4 and .csv data from OpenCamera Android app.
class DataLoader:
    def __init__(self, file_name):
        if file_name is None:
            raise Exception('No file name given')
        else:
            self.file_name = file_name
            self.imu_dict = None
            self.frame_metadata_dict = None
            try:
                self.start_time = os.path.getctime(f'data/{self.file_name}.mp4')
            except ImportError:
                raise Exception('No creation time found.')

    def load_mp4_and_dump_npy(self):
        # import mp4 file
        cap = cv2.VideoCapture(f'data/{self.file_name}.mp4')
        fps = cap.get(cv2.CAP_PROP_FPS)

        nframe = 0
        meta_data = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                break

            frame_array = np.array(gray_frame)

            np.save(open(f'data/record/images/frame_{nframe:06d}.npy', 'wb'), frame_array)

            cv2.imshow('frame', gray_frame)
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
        self.frame_metadata_dict = {
            'ts': meta_data
        }

    def load_csv_files(self):

        data = np.genfromtxt(f'data/{self.file_name}accel.csv', delimiter=',')
        accel_data = data[:, :-1]

        data = np.genfromtxt(f'data/{self.file_name}gyro.csv', delimiter=',')
        gyro_data = data[:, :-1]

        # create a new column with timeseries of imu data
        time_series_accel = np.linspace(self.start_time, self.frame_metadata_dict['ts'][-1], len(accel_data))
        time_series_gyro = np.linspace(self.start_time, self.frame_metadata_dict['ts'][-1], len(gyro_data))

        accel_data = np.hstack((time_series_accel.reshape(-1, 1), accel_data))
        gyro_data = np.hstack((time_series_gyro.reshape(-1, 1), gyro_data))

        imu_data = {
            'accel': accel_data, 'gyro': gyro_data
        }

        self.imu_dict = imu_data

    def dump_pickles(self):
        pickle.dump(self.imu_dict, open("data/record/imu.pickle", "wb"))
        pickle.dump(self.frame_metadata_dict, open("data/record/frame_metadata.pickle", "wb"))

    # input -> output : file_name -> imu, frame_metadata, npy dump
    def dump_files(self):
        self.load_mp4_and_dump_npy()
        self.load_csv_files()  # load fixed imu data
        self.dump_pickles()


if __name__ == '__main__':

    # parser name
    parser = argparse.ArgumentParser(description='Description of your program')

    # arguments
    parser.add_argument('-f', '--file', type=str, help='name of input file')

    # parsing with error cases
    try:
        args = parser.parse_args()
    except NameError:
        print("Error in parsing file name")
        sys.exit(1)
    else:
        # check number of args
        if len(vars(args)) != 1:
            parser.error('Invalid number of arguments.')
        else:
            # get file name
            file_id = args.file

            # run function to import csv data
            print(f'file id := {file_id}')
            dataLoader = DataLoader(file_id)
            dataLoader.dump_files()
