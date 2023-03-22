# MonocularVisionDepthEstimation
A Project that primarily uses mono vision cameras and auxiliary sensors to estimate depth of scenes.

## Format to generate np array and pickle data
1. Place `.mp4` video and `.csv` data in the `data/` directory.
2. Ensure each of the files has header _OpenCamera_ generates. _eg: VID_20230321_161057_
3. Run the `generate_cam_data.py` file from the root of the project and give ensure the following format and include the `-f` flag.
4. ```commandline
   python.exe .\src\generate_cam_data.py -f VID_20230321_161057
   ```
5.