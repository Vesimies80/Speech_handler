
import time
import numpy as np
import speech_recognition as sr
import pyaudio


class RecordingClass():
    def __init__(self, samplerate=48000) -> None:
        self.r = sr.Recognizer()
        self.samplerate = samplerate
        self.text = ""
    def start_recording(self):
        with sr.Microphone(sample_rate=self.samplerate) as source:
            while ("Appelsiini" and "appelsiini") not in self.text:
        # Adjust for ambient noise
                self.r.adjust_for_ambient_noise(source)
                print("Say something")

        # Listen for speech with timeout
                audio = None
                self.text = ""
                audio = self.r.listen(source, phrase_time_limit=10)
                try:
                    self.text = self.r.recognize_google(audio, language='fi')
                    print(f"You said: {self.text}")
                except sr.UnknownValueError:
                    pass
                except sr.exceptions.WaitTimeoutError:
                    pass
        return

def main():
    
    sample_rate = 48000
    
    rec = RecordingClass(sample_rate)
    print("Setup done")
    rec.start_recording()
    print("Recording done")
        

if __name__ == "__main__":
    main()
