import cv2
import logging
import queue
import time
import threading
from robodog.threads.VoiceCommandsThread import VoiceCommandsThread
from robodog.threads.SpeakerThread import SpeakerThread
from robodog.threads.VideoCaptureThread import VideoCaptureThread
from robodog.threads.BgSubtractionThread import BgSubtractionThread
#from robodog.threads.WebAppThread import WebAppThread
from robodog.utils.Statistics import Statistics

stop_signal = threading.Event()

# queues
frames_queue = queue.Queue(maxsize=5)
processed_frames = queue.Queue(maxsize=5)
voice_queue = queue.Queue(maxsize=5)

# threads
video_capture = VideoCaptureThread(stop_signal, 0, frames_queue)
video_capture.start()

bg_subtractor = BgSubtractionThread(stop_signal, frames_queue, processed_frames)
bg_subtractor.start()

voice_commands = VoiceCommandsThread(stop_signal, voice_queue)
voice_commands.start()

speaker = SpeakerThread(stop_signal, voice_queue)
speaker.start()

#web_app = WebAppThread(stop_signal, processed_frames)
#web_app.start()

# main loop
while not stop_signal.is_set():
    try:
        try:
            frame = processed_frames.get(timeout=2)
            if frame is None:
                pass
            cv2.imshow('Object Detection', frame)
        except queue.Empty:
                pass

        if cv2.waitKey(10) & 0xFF == ord('q'):
            stop_signal.set()
            break
    except Exception as e:
        logging.error(f"An exception was raised in the main thread: {e}")
        break

logging.info("Exiting...")
time.sleep(5)
logging.info("Stopped")
