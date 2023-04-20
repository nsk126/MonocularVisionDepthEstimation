import sys
import pyzed.sl as sl
import json
from signal import signal, SIGINT

cam = sl.Camera()

all_sensors_data_serialized = []

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    final_json = {}
    final_json["Sensors"] = all_sensors_data_serialized
    output_file = open("Sensors.json", 'w')
    json.dump(final_json, output_file, indent=4)
    output_file.close()
    print("Data were saved into ./Sensors.json")
    sys.exit(0)

signal(SIGINT, handler)


def IMUDataToJSON(imu_data):
    out = {}
    out["timestamp"] = imu_data.timestamp.get_nanoseconds()

    out["angular_velocity"] = [0, 0, 0]
    out["angular_velocity"][0] = imu_data.get_angular_velocity()[0]
    out["angular_velocity"][1] = imu_data.get_angular_velocity()[1]
    out["angular_velocity"][2] = imu_data.get_angular_velocity()[2]

    out["linear_acceleration"] = [0, 0, 0]
    out["linear_acceleration"][0] = imu_data.get_linear_acceleration()[0]
    out["linear_acceleration"][1] = imu_data.get_linear_acceleration()[1]
    out["linear_acceleration"][2] = imu_data.get_linear_acceleration()[2]
    return out

def SensorsDataToJSON(sensors_data):
    out = {}
    out["imu"] = IMUDataToJSON(sensors_data.get_imu_data())
    if(sensors_data.camera_moving_state == sl.CAMERA_MOTION_STATE.STATIC):
        out["camera_moving_state"] = "STATIC"
    if(sensors_data.camera_moving_state == sl.CAMERA_MOTION_STATE.MOVING):
        out["camera_moving_state"] = "MOVING"
    if(sensors_data.camera_moving_state == sl.CAMERA_MOTION_STATE.FALLING):
        out["camera_moving_state"] = "FALLING"
    out["image_sync_trigger"] = sensors_data.image_sync_trigger
    return out

def main():
    if not sys.argv or len(sys.argv) != 2:
        print("Only the path of the output SVO file should be passed as argument.")
        exit(1)

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.VGA
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    imu_data_grabbed_number = 0
    old_imu_timestamp = 0

    path_output = sys.argv[1]
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            frames_recorded += 1
            sensor_data = sl.SensorsData()
            if (cam.get_sensors_data(sensor_data, sl.TIME_REFERENCE.CURRENT)):
                if (old_imu_timestamp != sensor_data.get_imu_data().timestamp):
                    old_imu_timestamp = sensor_data.get_imu_data().timestamp
                    imu_data_grabbed_number += 1
                    sensors_data_serialized = SensorsDataToJSON(sensor_data)
                    all_sensors_data_serialized.append(sensors_data_serialized)
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    main()