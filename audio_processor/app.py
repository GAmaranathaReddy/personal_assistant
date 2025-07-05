import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import core logic classes
# Assuming src is in PYTHONPATH or we adjust path. For Streamlit, it's common to run from project root.
from src.audio_recorder import AudioRecorder
from src.transcriber import Transcriber as WhisperTranscriber
from src.text_processor import TextProcessor
from src.teams_poster import TeamsPoster

# --- Page Configuration (Optional but good practice) ---
st.set_page_config(
    page_title="Audio Processor Pro",
    page_icon="🎙️",
    layout="wide"
)

# --- Application State Initialization ---
# Using st.session_state to hold data across reruns
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'action_items' not in st.session_state:
    st.session_state.action_items = ""
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'audio_file_path' not in st.session_state:
    st.session_state.audio_file_path = None


# --- Main UI ---
st.title("🎙️ Audio Processor Pro")
st.markdown("Record or upload audio, get transcripts, summaries, action items, and post to MS Teams.")

st.sidebar.header("Configuration")
# Note: For live recording in Streamlit, it's complex due to browser limitations.
# Typically, Streamlit apps handle uploads better.
# We'll focus on upload first, and placeholder for recording.

st.sidebar.subheader("Audio Input")
input_method = st.sidebar.radio("Choose audio input method:", ("Upload Audio File", "Record Audio (Basic)"))

# Placeholder for recorded audio data or path
temp_audio_filename = "temp_recorded_audio.wav"

if input_method == "Record Audio (Basic)":
    st.sidebar.info("Audio recording in the browser via Streamlit has limitations. This is a basic implementation.")
    duration = st.sidebar.slider("Select recording duration (seconds):", 1, 30, 5)
    if st.sidebar.button("Start Recording"):
        with st.spinner(f"Recording for {duration} seconds... Speak now!"):
            try:
                recorder = AudioRecorder()
                # Saving to a known temporary path
                # Ensure this path is accessible and cleaned up if necessary
                # For Streamlit cloud, file system access can be tricky. Local is fine.
                st.session_state.audio_file_path = recorder.record_audio(duration, temp_audio_filename)
                st.sidebar.success(f"Recording saved as {st.session_state.audio_file_path}")
                # Display the audio player for the recorded file
                st.audio(st.session_state.audio_file_path, format="audio/wav")
            except Exception as e:
                st.sidebar.error(f"Recording failed: {e}")
                st.error("Could not record audio. Please ensure you have a microphone and necessary permissions. Try uploading a file instead.")
                st.session_state.audio_file_path = None

elif input_method == "Upload Audio File":
    uploaded_file = st.sidebar.file_uploader("Upload a WAV audio file", type=['wav'])
    if uploaded_file is not None:
        # Save uploaded file to a temporary location to pass to Whisper
        # Whisper typically expects a file path.
        # Ensure this temp file is handled correctly (e.g. deleted after use if needed)
        # For Streamlit, uploaded_file is an UploadedFile object.
        with open(temp_audio_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.audio_file_path = temp_audio_filename
        st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully.")
        # Display the audio player for the uploaded file
        st.audio(st.session_state.audio_file_path, format="audio/wav")


st.sidebar.subheader("Models & Services")
# Allow user to specify Whisper model (could be advanced setting)
whisper_model_options = ["tiny", "base", "small", "medium", "large"] # Add more if needed
st.session_state.whisper_model = st.sidebar.selectbox("Select Whisper Model:", whisper_model_options, index=whisper_model_options.index("tiny"))

# Ollama settings (can be pre-filled from .env or user input)
st.session_state.ollama_model = st.sidebar.text_input("Ollama Model:", value=os.getenv("OLLAMA_MODEL", "llama2"))
st.session_state.ollama_host = st.sidebar.text_input("Ollama Host (optional):", value=os.getenv("OLLAMA_HOST", ""))


# --- Processing Area ---
st.header("Processing & Results")

process_button_disabled = not (st.session_state.audio_file_path and os.path.exists(st.session_state.audio_file_path))

if not process_button_disabled:
    st.write(f"Ready to process: `{os.path.basename(st.session_state.audio_file_path)}`")
else:
    st.info("Please upload or record an audio file to make it available for processing.")

if st.button("Process Audio", type="primary", disabled=process_button_disabled):
    st.session_state.processing_done = False # Reset flags
    st.session_state.transcript = ""
    st.session_state.summary = ""
        st.session_state.action_items = ""

        with st.spinner(f"Transcribing with Whisper ('{st.session_state.whisper_model}')... This may take a while..."):
            try:
                transcriber = WhisperTranscriber(model_name=st.session_state.whisper_model)
                if not transcriber.model:
                    st.error("Whisper model failed to load. Check model name and resources.")
                else:
                    transcript_text = transcriber.transcribe_audio(st.session_state.audio_file_path)
                    if "Error:" in transcript_text:
                        st.error(f"Transcription failed: {transcript_text}")
                    else:
                        st.session_state.transcript = transcript_text
                        st.success("Transcription complete!")
            except Exception as e:
                st.error(f"An error occurred during transcription: {e}")

        if st.session_state.transcript:
            with st.spinner(f"Processing text with Ollama ('{st.session_state.ollama_model}')..."):
                try:
                    ollama_client_host = st.session_state.ollama_host if st.session_state.ollama_host else None
                    text_processor = TextProcessor(
                        ollama_model_name=st.session_state.ollama_model,
                        ollama_host=ollama_client_host
                    )

                    st.session_state.summary = text_processor.summarize_text(st.session_state.transcript)
                    if "Error:" in st.session_state.summary:
                         st.warning(f"Summarization issue: {st.session_state.summary}")

                    st.session_state.action_items = text_processor.generate_action_items(st.session_state.transcript)
                    if "Error:" in st.session_state.action_items:
                        st.warning(f"Action item generation issue: {st.session_state.action_items}")

                    st.success("Text processing complete!")
                    st.session_state.processing_done = True
                except Exception as e:
                    st.error(f"An error occurred during text processing with Ollama: {e}")
else:
    st.info("Please upload or record an audio file to begin processing.")


# --- Display Results ---
if st.session_state.processing_done:
    st.subheader("Transcript")
    st.text_area("Transcript", st.session_state.transcript, height=200, disabled=True)

    st.subheader("Summary")
    st.text_area("Summary", st.session_state.summary, height=100, disabled=True)

    st.subheader("Action Items")
    st.text_area("Action Items", st.session_state.action_items, height=150, disabled=True)

    # --- MS Teams Integration ---
    if st.session_state.action_items and "Error:" not in st.session_state.action_items and "No specific action items found" not in st.session_state.action_items.lower() :
        st.markdown("---")
        st.subheader("Post to MS Teams")
        teams_webhook_url_env = os.getenv("MS_TEAMS_WEBHOOK_URL")
        teams_webhook_url = st.text_input("MS Teams Webhook URL (from .env or paste here):", value=teams_webhook_url_env if teams_webhook_url_env else "")

        if teams_webhook_url:
            if st.button("Post Action Items to Teams"):
                with st.spinner("Posting to MS Teams..."):
                    try:
                        poster = TeamsPoster(webhook_url=teams_webhook_url)
                        title = f"Action Items from Audio: {os.path.basename(st.session_state.audio_file_path) if st.session_state.audio_file_path else 'Uploaded/Recorded Audio'}"
                        success = poster.post_message(title, st.session_state.action_items)
                        if success:
                            st.success("Action items posted to MS Teams successfully!")
                        else:
                            st.error("Failed to post action items to MS Teams. Check console for details from TeamsPoster.")
                    except ValueError as ve:
                        st.error(f"Teams Poster Error: {ve}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred while posting to Teams: {e}")
        else:
            st.info("To post to MS Teams, set the MS_TEAMS_WEBHOOK_URL in your .env file or paste it above.")
    elif st.session_state.action_items: # If action_items has "No specific..." or an error
        st.info("No actionable items to post to MS Teams.")


# --- Footer or additional info ---
st.markdown("---")
st.markdown("Make sure Ollama is running and the specified models are available.")
st.markdown("For `ffmpeg` and `Whisper` setup, refer to the project's `README.md`.")

# To run this app:
# 1. Ensure all dependencies from requirements.txt are installed (including streamlit).
# 2. Navigate to the `audio_processor` directory in your terminal.
# 3. Run: `streamlit run app.py`
