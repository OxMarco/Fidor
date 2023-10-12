import queue
import logging
import cv2
from robodog.Thread import GenericThread

class QrReaderThread(GenericThread):  
    def name(self) -> str:
        return "Qr Reader Thread"

    def init(self):
        super().init()
        self.qrDecoder = cv2.QRCodeDetector()

    def main(self):
        try:
            frame = self.args[0].get(timeout=2)
            if frame is None:
                pass

            # Detect QR code in the image
            retval, decoded_info, points, _ = self.qrDecoder.detectAndDecodeMulti(frame)

            if retval:
                # Print the QR code's decoded data
                for info in decoded_info:
                    logging.info(f'Decoded Data: {info}')

        except queue.Empty:
            pass
