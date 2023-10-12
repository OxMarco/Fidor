import queue
import logging
import cv2
import numpy as np
from robodog.Thread import GenericThread

class VideoCaptureThread(GenericThread):
    def name(self) -> str:
        return "Video Capture Thread"

    def init(self):
        super().init()
        logging.debug("Loading calibration data...")
        with np.load('calibration_data.npz') as data:
            self.mtx = data['mtx']
            self.dist = data['dist']
            self.rvecs = data['rvecs']
            self.tvecs = data['tvecs']
        logging.debug("Calibration data loaded")

        logging.debug("Opening video capture...")
        self.cap = cv2.VideoCapture(self.args[0])
        logging.debug("Video capture opened")

    def main(self):
        ret, frame = self.cap.read()
        if not ret:
            logging.warn("Skipping frame")
            pass

        frame = cv2.undistort(frame, self.mtx, self.dist, None, self.mtx)

        try:
            self.args[1].put(frame, timeout=2)
        except queue.Full:
            logging.error("Queue is full")
            pass

    def stop(self):
        super().stop()
        self.cap.release()

    def detect_lighting_conditions(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = cv2.mean(gray_image)[0]
        std_deviation = np.std(gray_image)

        if mean_brightness < 100 and std_deviation < 50:
            return "Low light conditions"
        elif mean_brightness > 150 and std_deviation > 100:
            return "High contrast or overexposed conditions"
        else:
            return "Normal lighting conditions"

    def statistics(self):
        ret, frame = self.cap.read()
        if not ret:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            return {
                "frame_size": (width, height),
                "fps": int(self.cap.get(cv2.CAP_PROP_FPS)),
                "lighting_conditions": self.detect_lighting_conditions(frame),
            }
        else:
            logging.error("Error getting data from the video stream")
            return None
