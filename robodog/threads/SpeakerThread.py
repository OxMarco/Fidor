import time
import queue
from playsound import playsound
from gtts import gTTS
from robodog.Thread import GenericThread

audio_file = "speak.mp3"

class SpeakerThread(GenericThread):
    def name(self) -> str:
        return "Speaker Thread"

    def main(self):
        try:
            say = self.args[0].get(timeout=2)
            speech = gTTS(text=say, lang='en', tld='co.uk', slow=False)
            speech.save(audio_file)
            playsound(audio_file)
        except queue.Empty:
            pass
        time.sleep(2)
