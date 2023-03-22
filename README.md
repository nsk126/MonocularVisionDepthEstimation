# MonocularVisionDepthEstimation
A Project that primarily uses mono vision cameras and auxiliary sensors to estimate depth of scenes.

## Format to generate np array and pickle data
1. Place `.mp4` video and `.csv` data in the `data/` directory.
2. Ensure each of the files has header _OpenCamera_ generates. _eg: VID_20230321_161057_
3. Run the `generate_cam_data.py` file from the root of the project and give ensure the following format and include the `-f` flag.
4. ```commandline
   python.exe .\src\generate_cam_data.py -f VID_20230321_161057
   ```

## Program to plot results in pickle files
_Note: Files need to be in `data/record` for this to work_.

`python.exe .\src\plot_data.py -ap` will read accel data and print it. The program has the flags `-a`, `-g` and `-p` for accel, gyro and print each.