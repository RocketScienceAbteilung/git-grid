import argparse
import mido
import gitgrid.gridcontroller
import numpy as np
import cv2

parser = argparse.ArgumentParser()
parser.add_argument(
    '--controller', '-c',
    default="launchpad",
)
args = parser.parse_args()

tmp = gitgrid.gridcontroller.create(args.controller)
cap = cv2.VideoCapture(0)

def toggle(x, y, Message):
    onoff = bool(tmp.lights[x, y, 0])
    tmp.lights[x, y, :] = not onoff

tmp.lights[:, :, :] = 0
# tmp.buttons[:, :] = toggle

while True:
    ret, gray = cap.read()
    cv2.imshow('frame', gray)
    shape = tmp.lights.shape[:-1]
    tmp.lights[:, :, :] = np.asarray(cv2.resize(gray[:,:,::-1] / 256., shape))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
