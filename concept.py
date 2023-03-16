import pyaudio
import wave
import time
import numpy as np

class MyRecorder():
    
    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024) -> None:
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        
    def open(self, filename, mode='wb'):
        return RecordingClass(filename, mode, self.channels, self.rate,
                            self.frames_per_buffer)
    
class RecordingClass():
    def __init__(self, filename, mode, channels, rate, frames_per_buffer) -> None:
        self.fname = filename
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None
        self.myframes = np.array([])
        
    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()
        
    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.myframes = np.concatenate((self.myframes, audio_data))
            return in_data, pyaudio.paContinue
        return callback
        
    def start_recording(self):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        output=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        
    def stop_recording(self):
        print(self.myframes)
        self._stream.stop_stream()
        return self
    
    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()
        
    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile


def main():
    filename = "speech.wav"
    
    #Audio parameters
    channels = 1
    sr = 44100
    frames = 1024
    
    slep = 0.1
    counter = 0
    max_time = 3
    
    rec = MyRecorder(channels=channels, rate=sr, frames_per_buffer=frames)
    with rec.open(filename, 'wb') as recfile2:
        recfile2.start_recording()
        while max_time > counter:
            time.sleep(slep)
            counter += slep
        recfile2.stop_recording() 
    
        

if __name__ == "__main__":
    main()
