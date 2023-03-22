import argparse
import sys
import pickle
from matplotlib import pyplot as plt


def read_accel(to_print=False):
    # read accel data
    accel = pickle.load(open('data/record/imu.pickle', 'rb'))
    accel = accel['accel']

    if to_print:
        print(accel)

    ts = accel[:, 0]
    ax = accel[:, 1]
    ay = accel[:, 2]
    az = accel[:, 3]

    plt.figure()
    plt.plot(ts, ax)
    plt.plot(ts, ay)
    plt.plot(ts, az)
    plt.legend(['ax', 'ay', 'az'])
    plt.show()


def read_gyro(to_print=False):
    # read gyro data
    gyro = pickle.load(open('data/record/imu.pickle', 'rb'))
    gyro = gyro['gyro']

    if to_print:
        print(gyro)

    ts = gyro[:, 0]
    gx = gyro[:, 1]
    gy = gyro[:, 2]
    gz = gyro[:, 3]

    plt.figure()
    plt.plot(ts, gx)
    plt.plot(ts, gy)
    plt.plot(ts, gz)
    plt.legend(['gx', 'gy', 'gz'])
    plt.show()

    pass


if __name__ == '__main__':

    # parser name
    parser = argparse.ArgumentParser(description='Description of your program')

    # arguments
    parser.add_argument('-a', '--accel', dest='accel', action='store_true', help='plot accelerometer data')
    parser.add_argument('-g', '--gyro', dest='gyro', action='store_true', help='plot gyroscope data')
    parser.add_argument('-p', '--print', dest='print', action='store_true', help='plot gyroscope data')

    # parsing with error cases
    try:
        args = parser.parse_args()
    except NameError:
        print("Error in parsing file name")
        sys.exit(1)
    else:
        if args.accel:
            read_accel(args.print)

        if args.gyro:
            read_gyro(args.print)
