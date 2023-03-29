# MonocularVisionDepthEstimation
A Project that primarily uses mono vision cameras and 
auxiliary sensors to estimate depth of scenes.

## Virtual environment
To seperate installations between host machine and our project, 
in the project directory run:
```commandline
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```
`.venv/Scripts/activate` works in windows CMD, may require 
special settings to run on PowerShell. For Linux, 
`source .venv/bin/activate` should work. Version of python 
used is `Python 3.9.13`.

## Format to generate np array and pickle data
1. Place `.mp4` video and `.csv` data in the `data/` directory.
2. Ensure each of the files has header _OpenCamera_ generates. _eg: VID_20230321_161057_
3. Run the `generate_cam_data.py` file from the root of the project and give ensure the following format and include the `-f` flag.
4. ```commandline
   python.exe .\src\generate_cam_data.py -f VID_20230321_161057
   ```

## Program to plot results in IMU pickle files
_Note: Files need to be in `data/record` for this to work_.

`python.exe .\src\plot_data.py -ap` will read accel data and print it. The program has the flags `-a`, `-g` and `-p` for accel, gyro and print each.

## Calibration
1. To calibrate your lens and find camera intrinsics, Take multiple pictures from your device and place the pictures in the `calibrate_imgs/` dir. Any format(_png, jpg_) should work.
2. The pictures you take can be a chessboard of any dimension. By default it'll be an 9x6 chessboard. Any different size will require a change in `calibrate.py` in the `chessboardSize` parameter.
3. Ideally, the pictures have to be of a physical print of the chessboard. For more info, refer [Mark Jones's post](https://markhedleyjones.com/projects/calibration-checkerboard-collection).
4. On running `src/calibrate.py`, it will generate intrinsics in the form of 3 .pkl files in the `calibrate_imgs/intrinsics/` dir. Do not move or delete them as `src/generate_cam_data.py` is use it to run.
