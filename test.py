from pyvcam import pvc
from pyvcam.camera import Camera

pvc.init_pvcam()

cams = list(Camera.detect_camera())
print(cams)

cam = cams[0]
cam.open()

print("Opened")

cam.close()
pvc.uninit_pvcam()
print('poep')