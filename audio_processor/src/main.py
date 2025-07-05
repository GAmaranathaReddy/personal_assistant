from audio_recorder import AudioRecorder
from transcriber import Transcriber as WhisperTranscriber
from text_processor import TextProcessor
from teams_poster import TeamsPoster
import os
from dotenv import load_dotenv

def main():
    load_dotenv() # Load environment variables from .env file

    print("Audio Processor Application")
    print("---------------------------")
    print("IMPORTANT: Ensure 'openai-whisper' is installed and 'ffmpeg' is available in your system PATH.")
    print("Ensure your Ollama instance is running and the specified model (e.g., 'llama2') is pulled.")
    print("For MS Teams posting, ensure MS_TEAMS_WEBHOOK_URL is set in your .env file or environment.\n")

    # --- 1. Record Audio ---
    recorder = AudioRecorder()
    try:
        duration_str = input("Enter recording duration in seconds (e.g., 5, or 0 to skip recording and use existing 'recorded_audio.wav'): ")
        duration = int(duration_str)
    except ValueError:
        print("Invalid duration entered. Defaulting to 5 seconds.")
        duration = 5

    output_filename = "recorded_audio.wav"
    audio_file_to_process = None

    if duration > 0:
        print(f"\nPreparing to record for {duration} seconds. Speak into your microphone.")
        audio_file_to_process = recorder.record_audio(duration, output_filename)
        print(f"Audio recorded and saved to {audio_file_to_process}")
    elif os.path.exists(output_filename):
        audio_file_to_process = output_filename
        print(f"\nSkipping recording. Using existing file: {audio_file_to_process}")
    else:
        print(f"\nSkipping recording, but {output_filename} not found. Please record audio first or place the file.")
        return

    # --- 2. Transcribe Audio using Whisper ---
    print("\n--- Initializing Whisper Transcriber ---")
    # Using "tiny" model for faster processing, user can change to "base", "small", etc.
    transcriber = WhisperTranscriber(model_name="tiny")

    transcript = ""
    if transcriber.model: # Check if Whisper model loaded
        print(f"\n--- Transcribing Audio: {audio_file_to_process} ---")
        transcript_or_error = transcriber.transcribe_audio(audio_file_to_process)
        if "Error:" in transcript_or_error or not transcript_or_error.strip():
            print(f"Transcription result: {transcript_or_error}")
            print("Cannot proceed without a valid transcript.")
            return
        transcript = transcript_or_error
        print("\n--- Transcript ---")
        print(transcript)
        print("------------------")
    else:
        print("Whisper model not loaded. Cannot transcribe. Please check installation and model name.")
        print("You can try running 'python src/transcriber.py' directly to debug Whisper setup.")
        return

    if not transcript or transcript.isspace(): # Double check after potential error message
        print("\nNo valid transcript obtained. Skipping text processing and Teams posting.")
    else:
        # --- 3. Process Text using Ollama ---
        ollama_host = os.getenv("OLLAMA_HOST")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama2") # Allow overriding Ollama model via env
        print(f"\n--- Initializing Ollama Text Processor (Model: {ollama_model}) ---")
        text_processor = TextProcessor(ollama_model_name=ollama_model, ollama_host=ollama_host)

        summary = text_processor.summarize_text(transcript)
        print("\n--- Summary (from Ollama) ---")
        print(summary)
        print("-----------------------------")

        action_items = text_processor.generate_action_items(transcript)
        print("\n--- Action Items (from Ollama) ---")
        print(action_items)
        print("----------------------------------")

        # --- 4. Post Action Items to MS Teams ---
        if action_items and "Error:" not in action_items and "No specific action items found" not in action_items:
            teams_webhook_url = os.getenv("MS_TEAMS_WEBHOOK_URL")
            if teams_webhook_url:
                post_choice = input("Do you want to post these action items to MS Teams? (yes/no): ").strip().lower()
                if post_choice == 'yes':
                    try:
                        poster = TeamsPoster(webhook_url=teams_webhook_url)
                        # Try to get a filename for the title, or use a generic one
                        audio_basename = os.path.basename(audio_file_to_process)
                        teams_title = f"Action Items from: {audio_basename}"
                        post_successful = poster.post_message(teams_title, action_items)
                        if not post_successful:
                            print("There was an issue posting to MS Teams. Please check the logs above and your webhook URL.")
                    except ValueError as ve:
                        print(f"Error initializing Teams Poster: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred during Teams posting: {e}")
                else:
                    print("Skipping MS Teams post.")
            else:
                print("\nMS_TEAMS_WEBHOOK_URL not set. Skipping Teams posting.")
                print("To enable, set MS_TEAMS_WEBHOOK_URL in your .env file or environment variables.")
        elif "No specific action items found" in action_items:
            print("\nNo specific action items were generated, so nothing to post to MS Teams.")
        else:
            print("\nNo valid action items generated or an error occurred. Skipping MS Teams posting.")

    print("\nApplication processing complete.")

if __name__ == "__main__":
    main()
