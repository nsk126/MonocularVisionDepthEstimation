## to-do

- Try to undistorted feed before processing []
- Understand complete flow of code till observer []
- Integrate KF as a start - use filters.py []
- Try other filters[]
- Make live processing - either w zed or opencam[]
- check params.json[] in record dir[]
- #93 from `ttc_depth_from_folder.py` seems to be skipping a frame?[]
- RecordedIMUSource accouts for gyro bias[]
- Resamples the imu data using `scipy.interpolate.interp1d`[]
- #55 of `ttc_depth_from_folder.py` - responsible for resampling, need to read[]
- #302, #307, #313 - `AffineTrackRotInvariant`, 

---

## Claims:
1. TTCDist is not a replacment stack for VINS Mono or ROVIO. A repalcement would need the entire stack. TTCDist only provides 2 measurements phi and tau - which are comparable estimates.
2. The claim is that ttcdist in python is faster than vins mono and rovio in cpp by a considerable margin.


## I want to try:
1. Scan for good features to track
2. Create multiple patches and convert into a VIO framework

## key notes from paper:
- The affine tracker was initialized by tracking a 100×100 pixel patch sub-sampled to 4000 pixels. While the patch size changes dramatically during fixation, only 4000 pixels are drawn from each frame.