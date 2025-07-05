# Transcription functionality using Whisper
import os
try:
    import whisper
except ImportError:
    print("Whisper library not found. Please install it with 'pip install openai-whisper'")
    print("You also need to have ffmpeg installed on your system: https://ffmpeg.org/download.html")
    whisper = None # Set to None if import fails, so we can handle it gracefully

class Transcriber:
    def __init__(self, model_name="base"): # Whisper model name: "tiny", "base", "small", "medium", "large"
        self.model_name = model_name
        self.model = None
        if whisper:
            try:
                print(f"Loading Whisper model '{self.model_name}'...")
                self.model = whisper.load_model(self.model_name)
                print("Whisper model loaded successfully.")
            except Exception as e:
                print(f"Error loading Whisper model '{self.model_name}': {e}")
                print("Please ensure the model name is correct and you have enough resources.")
                self.model = None # Ensure model is None if loading fails
        else:
            print("Whisper library is not available. Transcription will not work.")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the given audio file using the loaded Whisper model.
        """
        if not self.model:
            return "Error: Whisper model not loaded. Cannot transcribe."

        if not os.path.exists(audio_file_path):
            return f"Error: Audio file {audio_file_path} not found."

        print(f"Transcribing {audio_file_path} using Whisper model '{self.model_name}'...")
        try:
            result = self.model.transcribe(audio_file_path, fp16=False) # fp16=False for wider CPU compatibility
            transcript = result["text"]
            print("Transcription complete.")
            return transcript
        except NameError: # If whisper module itself was not imported
             return "Error: Whisper library is not installed or failed to import. Cannot transcribe."
        except Exception as e:
            # This can catch errors if ffmpeg is not found, or other issues during transcription
            error_message = f"Error during Whisper transcription: {e}"
            if "ffmpeg" in str(e).lower():
                error_message += "\nThis might be due to ffmpeg not being installed or not found in PATH."
                error_message += "\nPlease install ffmpeg: https://ffmpeg.org/download.html"
            print(error_message)
            return error_message

if __name__ == '__main__':
    # This is a simple test and assumes:
    # 1. You have run `pip install openai-whisper`
    # 2. You have `ffmpeg` installed and in your system's PATH.
    # 3. You have an audio file named "recorded_audio.wav" or similar.

    # Create a dummy audio file for testing if it doesn't exist (won't be a real WAV)
    # For a real test, replace this with an actual audio file.
    dummy_file = "test_audio.wav"
    if not os.path.exists(dummy_file):
        try:
            # Attempt to create a tiny valid WAV file for basic testing if possible
            # This requires soundfile and numpy, which should be there from audio_recorder
            import soundfile as sf
            import numpy as np
            samplerate = 44100
            duration = 1 # 1 second
            frequency = 440 # A4 note
            t = np.linspace(0, duration, int(samplerate * duration), False)
            data = 0.5 * np.sin(2 * np.pi * frequency * t)
            # Ensure data is in correct format for WAV (e.g., int16)
            data_int16 = (data * 32767).astype(np.int16)
            sf.write(dummy_file, data_int16, samplerate)
            print(f"Created dummy WAV file {dummy_file} for testing.")
        except Exception as e:
            print(f"Could not create dummy WAV {dummy_file} for testing: {e}. Using a placeholder file.")
            # Fallback to simple text file if soundfile fails (e.g. not installed yet by user)
            with open(dummy_file, "w") as f:
                f.write("This is not a real audio file, Whisper will likely fail but test the script structure.")
            print(f"Created placeholder file {dummy_file}. Whisper will likely error on this.")


    print("\n--- Initializing Transcriber (using 'base' Whisper model) ---")
    # Using "tiny" or "base" for quicker testing. "base" is generally a good starting point.
    transcriber = Transcriber(model_name="tiny")

    if transcriber.model: # Check if model loaded successfully
        print(f"\n--- Transcribing {dummy_file} ---")
        transcript = transcriber.transcribe_audio(dummy_file)
        print("\n--- Transcript ---")
        print(transcript)
    else:
        print("\n--- Transcription Test Skipped: Whisper model failed to load ---")
        print("Please ensure 'openai-whisper' is installed and model files can be downloaded.")

    # To clean up the dummy file:
    # if os.path.exists(dummy_file):
    #     os.remove(dummy_file)
    #     print(f"Removed dummy file {dummy_file}")
