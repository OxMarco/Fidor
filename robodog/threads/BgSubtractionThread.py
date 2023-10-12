import queue
import logging
import cv2
from robodog.Thread import GenericThread

class BgSubtractionThread(GenericThread):  
    def name(self) -> str:
        return "Background Subtraction Thread"

    def init(self):
        super().init()
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=16, detectShadows=False)

    def main(self):
        try:
            frame = self.args[0].get(timeout=2)
            if frame is None:
                pass

            fg_mask = self.bg_subtractor.apply(frame)
            latest_bg_frame = cv2.bitwise_and(frame, frame, mask=fg_mask)
            self.args[1].put(latest_bg_frame, timeout=2)

        except queue.Empty:
            pass
