# Audio recording functionality
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class AudioRecorder:
    def __init__(self, samplerate=44100, channels=1):
        self.samplerate = samplerate
        self.channels = channels

    def record_audio(self, duration, output_filename="output.wav"):
        """Records audio for a specified duration and saves it to a file."""
        print(f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype='int16')
        sd.wait()  # Wait until recording is finished
        write(output_filename, self.samplerate, recording)  # Save as WAV file
        print(f"Recording saved to {output_filename}")
        return output_filename

if __name__ == '__main__':
    recorder = AudioRecorder()
    try:
        duration = int(input("Enter recording duration in seconds: "))
        filename = recorder.record_audio(duration)
    except ValueError:
        print("Please enter a valid number for duration.")
    except Exception as e:
        print(f"An error occurred: {e}")
