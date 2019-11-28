import os
import logging
import logging.handlers
import random
import sys

import numpy as np
import skvideo.io
import cv2
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import utils
# without this some strange errors happen
cv2.ocl.setUseOpenCL(False)
random.seed(123)

from pipeline import (
    PipelineRunner,
    ContourDetection,
    Visualizer,
    CsvWriter,
    VehicleCounter)

# ============================================================================
IMAGE_DIR = "./out"
VIDEO_SOURCE = None
if len(sys.argv) == 2:
    VIDEO_SOURCE = sys.argv[1]

SHAPE = (368, 640)  # HxW
EXIT_PTS = np.array([
# left side
#    [[0, 0], [50, 0], [50, 480], [0, 480]]
# right side
    [[540,0], [640,0],[640,368],[540,360]]
])
MIN_COUNTOUR_WIDTH = 100
MIN_COUNTOUR_HEIGHT = 35

# ============================================================================


def train_bg_subtractor_pi(bg, camera, rawCapture, num=500):
    '''
        BG substractor need process some amount of frames to start giving result
    '''
    print ('Training BG Subtractor on pi video stream...')
    # allow the camera to warmup
    time.sleep(0.1)
    count = 0 
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        bg.apply(image, None, 0.001)
 
        # show the frame
        cv2.imshow("Frame", image)
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # if the `q` key was pressed, break from the loop
        if count > num:
            break
        count += 1

    print ('Finishing training BG Subtractor')

def train_bg_subtractor_video(bg, cap, num=500):
    '''
        BG substractor need process some amount of frames to start giving result
    '''
    print ('Training BG Subtractor on input video...')
    # allow the camera to warmup
    time.sleep(0.1)
    count = 0 
    # capture frames from the camera
    for frame in cap:
        bg.apply(frame, None, 0.001)
        count += 1
        if count >= num:
            return cap

    print ('Finishing training BG Subtractor')
def run_pi(pipeline, camera, rawCapture):
    
    print ('Running detection model in pi video stream...')
    _frame_number = -1
    frame_number = -1
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
#        if not frame.any():
#            log.error("Frame capture failed, stopping...")
#            break

        # real frame number
        _frame_number += 1

        # skip every 2nd frame to speed up processing
        if _frame_number % 2 != 0:
            rawCapture.truncate(0)
            continue

        # frame number that will be passed to pipline
        # this needed to make video from cutted frames
        frame_number += 1

        # plt.imshow(frame)
        # plt.show()
        # return

        pipeline.set_context({
            'frame': image,
            'frame_number': frame_number,
        })

        pipeline.run()
        # clear the stream in preparation for the next frame
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break

def run_video(pipeline, cap):

    print ('Running detection model on input video...')
    _frame_number = -1
    frame_number = -1
    for frame in cap:
        if not frame.any():
            log.error("Frame capture failed, stopping...")
            break

        # real frame number
        _frame_number += 1

        # skip every 2nd frame to speed up processing
        if _frame_number % 2 != 0:
            continue

        # frame number that will be passed to pipline
        # this needed to make video from cutted frames
        frame_number += 1

        # plt.imshow(frame)
        # plt.show()
        # return

        pipeline.set_context({
            'frame': frame,
            'frame_number': frame_number,
        })
        image = pipeline.run()

def main():
    log = logging.getLogger("main")

    # creating exit mask from points, where we will be counting our vehicles
    base = np.zeros(SHAPE + (3,), dtype='uint8')
    exit_mask = cv2.fillPoly(base, EXIT_PTS, (255, 255, 255))[:, :, 0]

    # there is also bgslibrary, that seems to give better BG substruction, but
    # not tested it yet
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500, detectShadows=True)

    # processing pipline for programming conviniance
    pipeline = PipelineRunner(pipeline=[
        ContourDetection(bg_subtractor=bg_subtractor,
                        min_contour_width=MIN_COUNTOUR_WIDTH, 
                        min_contour_height=MIN_COUNTOUR_HEIGHT,
                         save_image=True, image_dir=IMAGE_DIR),
        # we use y_weight == 2.0 because traffic are moving vertically on video
        # use x_weight == 2.0 for horizontal.
        VehicleCounter(exit_masks=[exit_mask], x_weight=2.0),
        Visualizer(image_dir=IMAGE_DIR),
       # CsvWriter(path='./', name='report.csv')
    ], log_level=logging.DEBUG)

    # Set up image source
    # You can use also CV2, for some reason it not working for me
#    cap = skvideo.io.vreader(VIDEO_SOURCE)

    # skipping 500 frames to train bg subtractor
    if VIDEO_SOURCE:
        cap = skvideo.io.vreader(VIDEO_SOURCE)
        train_bg_subtractor_video(bg_subtractor, cap, num=500)
        cap = skvideo.io.vreader(VIDEO_SOURCE)
        run_video(pipeline, cap)
    else:
        camera = PiCamera()
        camera.resolution = (640, 368)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 368))
        # allow the camera to warmup
        time.sleep(0.1)
        train_bg_subtractor_pi(bg_subtractor, camera, rawCapture, num=500)
        run_pi(pipeline, camera, rawCapture)
        cap.release()
        cv2.destroyAllWindows()
        
#    cap = skvideo.io.vreader(VIDEO_SOURCE)



# ============================================================================

if __name__ == "__main__":
    log = utils.init_logging()

    if not os.path.exists(IMAGE_DIR):
        log.debug("Creating image directory `%s`...", IMAGE_DIR)
        os.makedirs(IMAGE_DIR)

    main()
