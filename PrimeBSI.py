import numpy as np
import time
from pyvcam import pvc
from pyvcam.camera import Camera


class PrimeBSICamera:
    def __init__(self):
        self.cam = None
        self.is_open = False
        self.live_mode = False

    # ----------------------------
    # Initialization / Connection
    # ----------------------------
    def initialize(self):
        pvc.init_pvcam()

    def shutdown(self):
        pvc.uninit_pvcam()

    def open(self, camera_name=None, exposure_mode=0):
        cams = list(Camera.detect_camera())
        print(cams)

        if not cams:
            raise RuntimeError("No cameras detected")

        if camera_name is None:
            self.cam = cams[0]
        else:
            self.cam = next((c for c in cams if c.name == camera_name), None)
            if self.cam is None:
                raise ValueError(f"Camera '{camera_name}' not found")

        self.cam.open()

        self.cam.exp_mode = 'Internal Trigger'
        self.cam.readout_port = 0
        self.cam.speed_table_index = 0
        self.cam.gain = 1
        self.cam.exp_time = 10  # ms

        self.is_open = True

    def close(self):
        if self.cam and self.is_open:
            self.cam.close()
            self.is_open = False

    # ----------------------------
    # Configuration
    # ----------------------------
    def set_exposure(self, exposure_ms):
        """Set exposure time in milliseconds"""
        self.cam.exp_time = int(exposure_ms)

    def set_roi(self, x, y, width, height):
        """Set region of interest"""
        self.cam.roi = (x, y, width, height)

    def set_binning(self, bin_x=1, bin_y=1):
        """Set binning"""
        self.cam.binning = (bin_x, bin_y)

    def get_sensor_size(self):
        return self.cam.sensor_size

    # ----------------------------
    # Acquisition
    # ----------------------------
    def start_live(self):
        """Start continuous acquisition"""
        self.cam.start_live()
        self.live_mode = True

    def stop_live(self):
        if self.live_mode:
            try:
                self.cam.abort()   # force stop (better than finish)
            except Exception:
                pass

            try:
                self.cam.finish()
            except Exception:
                pass

            self.live_mode = False

    def snap(self, timeout=2.0):

        # Ensure internal trigger (use your working value, likely 1792)
        self.cam.exp_mode = 'Internal Trigger'
        self.cam.readout_port = 0
        self.cam.speed_table_index = 0
        self.cam.gain = 1

        # Start acquisition explicitly
        self.cam.start_live()
        self.live_mode = True

        try:
            start = time.time()

            while True:
                frame = self.cam.poll_frame()

                if frame is not None:
                    return np.array(frame['pixel_data'], dtype=np.uint16)

                if time.time() - start > timeout:
                    raise TimeoutError("Snap timed out")

                time.sleep(0.005)

        finally:
            self.stop_live()

    # ----------------------------
    # Single Image Acquisition
    # ---------------------------

    # ----------------------------
    # Sequence Acquisition
    # ----------------------------
    def acquire_sequence(self, num_frames):
        """Acquire a sequence of images"""
        frames = self.cam.get_sequence(num_frames)
        return np.array(frames, dtype=np.uint16)

    # ----------------------------
    # Utility
    # ----------------------------
    def get_temperature(self):
        return self.cam.temp

    def get_gain(self):
        return self.cam.gain

    def set_gain(self, gain):
        self.cam.gain = gain



if __name__ == "__main__":
    cam = PrimeBSICamera()
    print('initializing camera')
    cam.initialize()
    cam.open()

    print("Ports:", cam.cam.readout_ports)
    print("Speeds:", cam.cam.speed_table_index)
    print("Gain:", cam.cam.gain)

    #perform testimage
    print('perform testimage')
    img = cam.cam.get_frame()
    print(img.shape)

    

    #print('setting_exposure')
    #cam.set_exposure(50)  # 50 ms

    # Snap single image
    #print('snapping_image')
    #image = cam.snap()
    #print("Image shape:", image.shape)

    # Live mode
    #cam.start_live()
    #frame = cam.get_live_frame()
    #cam.stop_live()

    # Sequence
    #print('sequence')
    #stack = cam.acquire_sequence(10)
    #print("Stack shape:", stack.shape)

    cam.close()
    cam.shutdown()
    