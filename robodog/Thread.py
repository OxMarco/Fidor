import logging
import threading
import time

logging.basicConfig(level=logging.INFO)

class GenericThread(threading.Thread):
    def __init__(self, stop_signal, *args, **kwargs):
        super(GenericThread, self).__init__()
        self.stop_signal = stop_signal
        self.is_running = False
        self.args = args
        self.kwargs = kwargs

    def name(self) -> str:
        raise NotImplementedError("Child classes should override this method")

    def init(self):
        logging.info(f"{self.name()} starting.")
        self.is_running = True

    def run(self):
        try:
            self.init()
            previousTime = 0
            currentTime = 0
            while not self.stop_signal.is_set() and self.is_running:
                self.main()
                
                currentTime = time.time()
                self.fps = 1 / (currentTime-previousTime)
                previousTime = currentTime
        except Exception as e:
            logging.error(f"{self.name()} encountered an exception: {e}")
        finally:
            logging.info(f"{self.name()} stopped.")

    def main(self):
        raise NotImplementedError("Child classes should override this method")

    def stop(self):
        logging.info(f"{self.name()} stopping.")
        self.is_running = False

    def fps(self):
        return self.fps
