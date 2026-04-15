import MuDMInterface as MuDM
from PrimeBSI import PrimeBSICamera
import time

# open camera and print some info
cam = PrimeBSICamera()
cam.initialize()
cam.open()

print("Ports:", cam.cam.readout_ports)
print("Speeds:", cam.cam.speed_table_index)
print("Gain:", cam.cam.gain)

#perform testimage
print('perform testimage')
img = cam.cam.get_frame()
print(img.shape)