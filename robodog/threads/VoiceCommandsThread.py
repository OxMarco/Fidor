import time
import logging
import speech_recognition as sr
from robodog.Thread import GenericThread

class VoiceCommandsThread(GenericThread):
    def name(self) -> str:
        return "Voice Commands Thread"

    def init(self):
        super().init()
        self.recognizer = sr.Recognizer()

    def main(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=5)
            logging.info("Waiting for vocal command... Speak now!")

            try:
                # Record audio
                audio_data = self.recognizer.listen(source)
                data = self.recognizer.recognize_google(audio_data)
                logging.info("You said: " + data)
                self.parse_command(data)
            except sr.UnknownValueError:
                logging.error("Could not understand audio")
                
            except sr.RequestError as e:
                logging.error(f"Could not request results; {e}")
        time.sleep(5)

    def parse_command(self, text):
        # TODO add openai for interpreting commands
        if(text == "hello"):
            self.args[0].put("Hello!", timeout=2)
        elif(text == "goodbye"):
            self.args[0].put("Goodbye!", timeout=2)
            # terminate all threads
            self.stop_signal.set()
