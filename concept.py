import pyaudio
import wave
import time
import numpy as np
import speech_recognition as sr

def pcm2float(sig, dtype='float32'):
    """Convert PCM signal to floating point with a range from -1 to 1.
    Use dtype='float32' for single precision.
    Parameters
    ----------
    sig : array_like
        Input array, must have integral type.
    dtype : data type, optional
        Desired (floating point) data type.
    Returns
    -------
    numpy.ndarray
        Normalized floating point data.
    See Also
    --------
    float2pcm, dtype
    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be a floating point type")

    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig.astype(dtype) - offset) / abs_max

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
        self.r = sr.Recognizer()
        
    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()
        
    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            audio_data = np.frombuffer(in_data, dtype='<i2')
            #audio_data = pcm2float(audio_data)
            audio_data = sr.AudioData(audio_data, sample_rate=self.rate, sample_width=1)
            #audio_data = self.r.record(in_data)
            text = self.r.recognize_sphinx(audio_data)
            print(text)
            
            return in_data, pyaudio.paContinue
        return callback
        
    def start_recording(self):
        #self._stream = self._pa.open(format=pyaudio.paInt16,
        #                                channels=self.channels,
        ##                                rate=self.rate,
        #                                input=True,
        #                                output=True,
        #                                frames_per_buffer=self.frames_per_buffer,
        #                                stream_callback=self.get_callback())
        with sr.Microphone() as source:

    # Adjust for ambient noise
            self.r.adjust_for_ambient_noise(source)
            print("Say something...")

    # Listen for speech with timeout
            audio = self.r.listen(source, timeout=5)
            text = self.r.recognize_sphinx(audio)
            print(f"You said: {text}")

    def stop_recording(self):
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
    sr = 16000
    frames = 4096
    
    slep = 0.1
    counter = 0
    max_time = 10
    
    rec = MyRecorder(channels=channels, rate=sr, frames_per_buffer=frames)
    with rec.open(filename, 'wb') as recfile2:
        recfile2.start_recording()
        while max_time > counter:
            time.sleep(slep)
            counter += slep
        recfile2.stop_recording() 
    
        

if __name__ == "__main__":
    main()
