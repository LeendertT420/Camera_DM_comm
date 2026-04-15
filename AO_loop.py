from MuDMInterface import MuDMInterface, actuator_count, zernikes_count
from PrimeBSI import PrimeBSICamera
from image_sharpness_measures import compute_local_variance, compute_tenengrad, compute_brenner_gradient
import time
import numpy as np

############################################
##### open camera and print some info ######
############################################

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


###################################
##### open deformable mirror ######     
###################################

DM = MuDMInterface()
DM.connect('0027')

temp = DM.get_temperature()
print("Temperature Received :"+str(temp))

test = DM.get_overheat_status()
if test :
    outstr = ("Mirror Overheated and Stopped!")
else:
    outstr = ("Mirror Working Normally")



########################
##### run AO loop ######
########################

N_iterations = 10
N_modes = 10
scan_range = np.linspace(-1, 1, 10)  # Example scan range for each Zernike mode

loss_function = compute_brenner_gradient  # Example loss function, replace with actual implementation

zernike_coeffs = np.zeros(N_modes)

for n in range(N_iterations):
    for k in range(N_modes):
        best_value = None
        best_metric = float('inf')

        for amp in scan_range:
            zernike_coeffs[k] = amp

            DM.move_to_zernike_surface(zernike_coeffs, zernike_coeffs[4])

            image = cam.acquire_image()
            loss_metric = loss_function(image)

            if loss_metric < best_metric:
                best_metric = loss_metric
                best_value = amp

        # lock in best value
        zernike_coeffs[k] = best_value

DM.disconnect()
del DM