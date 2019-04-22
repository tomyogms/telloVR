# Reference link: https://face-recognition.readthedocs.io/en/latest/face_recognition.html#module-face_recognition.api

import face_recognition
from PIL import Image
import cv2
import os
import sys
import time
from drone_ui import DroneUI
import tello


def main():
    drone = tello.Tello('', 8889)
    #drone._receive_video_thread()
    drone = DroneUI(drone)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()