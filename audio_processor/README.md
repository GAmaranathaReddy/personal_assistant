# Audio Processor CLI

This Python application records audio, transcribes it, generates a summary and action items using AI, and can post these action items to a Microsoft Teams channel.

## Features

-   **Audio Recording**: Captures audio from your microphone.
-   **Transcription**: Converts spoken audio into text using `openai-whisper`.
-   **Summarization**: Generates a concise summary of the transcript using a local LLM via Ollama.
-   **Action Item Generation**: Extracts actionable tasks from the transcript using Ollama.
-   **MS Teams Integration**: Posts generated action items to a specified MS Teams channel via an Incoming Webhook.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: Ensure Ollama is installed and running. You can download it from [https://ollama.com/](https://ollama.com/).
    -   Pull a model for text processing, e.g., `llama2` or `mistral`:
        ```bash
        ollama pull llama2
        ollama pull mistral
        ```
3.  **ffmpeg**: `openai-whisper` requires `ffmpeg` to be installed on your system and available in your PATH.
    -   On macOS: `brew install ffmpeg`
    -   On Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
    -   On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Setup

1.  **Clone the repository (if applicable) or download the files.**

2.  **Navigate to the project directory:**
    ```bash
    cd audio_processor
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This installs all necessary libraries, including `streamlit` for the web UI, `openai-whisper` for transcription, `ollama` for LLM interactions, etc.
    *Note: `openai-whisper` and its dependencies (like PyTorch) can be large. Ensure you have sufficient disk space and a stable internet connection during installation.*

5.  **Configure Environment Variables:**
    Create a `.env` file in the `audio_processor` directory (i.e., at the same level as `app.py`, `src/` and `requirements.txt`).
    Add the following variables as needed:

    ```env
    # Required for posting to MS Teams (if you want to use this feature)
    MS_TEAMS_WEBHOOK_URL="your_ms_teams_incoming_webhook_url_here"

    # Optional: Specify the Ollama host if it's not running on localhost or default port
    # OLLAMA_HOST="http://localhost:11434"

    # Optional: Specify a different Ollama model for summarization/action items
    # OLLAMA_MODEL="mistral"
    ```
    -   To get an `MS_TEAMS_WEBHOOK_URL`:
        1.  Go to the desired channel in MS Teams.
        2.  Click on the three dots (...) for 'More options'.
        3.  Select 'Connectors'.
        4.  Search for 'Incoming Webhook' and click 'Configure' or 'Add'.
        5.  Provide a name (e.g., "AudioProcessorApp") and click 'Create'.
        6.  Copy the generated Webhook URL.
        7.  Paste this URL into your `.env` file.

## Running the Application

The application now features a Streamlit web interface.

1.  **Ensure your virtual environment is activated.**
2.  **Make sure Ollama is running with the model you intend to use (e.g., `llama2`, or the one specified in `OLLAMA_MODEL` in your `.env` file).**
3.  **Navigate to the `audio_processor` directory (if not already there).**
4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
5.  **Open your web browser** to the local URL provided by Streamlit (usually `http://localhost:8501`).
6.  **Use the web interface:**
    -   Choose to upload an audio file (WAV) or use the basic recording feature in the sidebar.
    -   Configure Whisper and Ollama models in the sidebar if needed.
    -   Click "Process Audio".
    -   View the transcript, summary, and action items.
    -   Optionally, enter your MS Teams webhook URL (if not in `.env`) and post the action items.

### Legacy CLI (Still Available)

The original command-line interface is still available if preferred:

1.  **Ensure your virtual environment is activated and Ollama is running.**
2.  **Run the main script from the `audio_processor` directory:**
    ```bash
    python src/main.py
    ```
3.  **Follow the on-screen prompts.**


## Project Structure

```
audio_processor/
├── app.py                    # Main Streamlit application script
├── src/
│   ├── __init__.py
│   ├── main.py               # Original CLI application script
│   ├── audio_recorder.py     # Handles audio recording
│   ├── transcriber.py        # Handles audio transcription using Whisper
│   ├── text_processor.py     # Handles summarization and action items via Ollama
│   └── teams_poster.py       # Handles posting to MS Teams
├── tests/                    # (Placeholder for future tests)
├── scripts/                  # (Placeholder for utility scripts)
├── requirements.txt          # Python package dependencies
├── .env                      # For environment variables (MS_TEAMS_WEBHOOK_URL, etc.) - YOU CREATE THIS
└── README.md                 # This file
```

## Notes on Whisper and Ollama Models

-   The application currently defaults to using the "tiny" Whisper model for faster processing (`transcriber.py`).
-   You can change the model size (e.g., "base", "small", "medium", "large") in `src/transcriber.py` (in the `WhisperTranscriber` constructor or when `main.py` instantiates it) for better accuracy, but this will require more resources and time. The first time you use a new model, Whisper will download it.

## Troubleshooting

-   **`No space left on device` during `pip install`**: Free up disk space. PyTorch (a dependency of Whisper) is large.
-   **Whisper/ffmpeg errors**: Ensure `ffmpeg` is correctly installed and in your system's PATH. Run `ffmpeg -version` in your terminal to check.
-   **Ollama connection errors**:
    -   Verify Ollama is running: `ollama list`
    -   Ensure the model specified (e.g., `llama2`) is pulled.
    -   If Ollama is on a different host/port, set `OLLAMA_HOST` in your `.env` file.
-   **MS Teams Posting Fails**:
    -   Double-check the `MS_TEAMS_WEBHOOK_URL` in your `.env` file.
    -   Ensure the webhook is still active in your Teams channel.
    -   Check for firewall issues that might block outgoing requests.
```
