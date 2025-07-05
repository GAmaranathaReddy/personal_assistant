# Agent Guidance for Audio Processor CLI

Hello Agent! This file provides guidance for working on the Audio Processor CLI project.

## Core Technologies

-   **Python**: The primary language.
-   **`openai-whisper`**: Used for speech-to-text transcription. Requires `ffmpeg`.
-   **Ollama**: Used for running local LLMs (e.g., `llama2`, `mistral`) for text summarization and action item generation.
-   **MS Teams Incoming Webhooks**: Used for posting messages to Teams.
-   **`sounddevice`**: For audio recording.

## Development Guidelines

1.  **Environment Variables**:
    -   Sensitive information like the MS Teams Webhook URL and potentially Ollama host/model preferences are managed via a `.env` file. See `README.md` for details on which variables are used.
    -   Do not commit `.env` files. A `.gitignore` should be in place to prevent this (though not explicitly created by you in this session, it's standard practice).

2.  **Dependencies**:
    -   All Python dependencies are listed in `requirements.txt`.
    -   If you add new dependencies, update this file: `pip freeze > requirements.txt` (after installing in your virtual environment).
    -   Be mindful of system dependencies like `ffmpeg`.

3.  **Code Structure**:
    -   The code is organized into modules within the `src/` directory:
        -   `main.py`: Main application entry point and orchestration.
        -   `audio_recorder.py`: Audio input.
        -   `transcriber.py`: Speech-to-text.
        -   `text_processor.py`: LLM-based text analysis (summary, action items).
        -   `teams_poster.py`: MS Teams communication.
    -   Try to keep functionality within the appropriate module.

4.  **Error Handling**:
    -   Provide user-friendly error messages.
    -   Gracefully handle potential issues like missing dependencies (e.g., Whisper not installed, ffmpeg not found), Ollama connection problems, or invalid Teams webhook URLs. The current implementation attempts this; maintain or improve it.

5.  **User Interaction**:
    -   The primary interface is CLI-based (`main.py`). Keep prompts and outputs clear.
    -   Confirm potentially sensitive actions (like posting to Teams, though currently, it's an explicit choice after items are shown).

6.  **Testing**:
    -   (Currently, formal unit tests are placeholders). If adding features, consider adding corresponding tests in the `tests/` directory.
    -   Manual testing of the end-to-end flow is crucial:
        -   Recording audio.
        -   Transcription quality with Whisper (consider testing different Whisper models).
        -   Ollama processing (summary and action item quality with different Ollama models).
        -   Teams posting.

7.  **README.md**:
    -   Keep `README.md` updated with setup instructions, prerequisites, and how to run the application. This is the primary guide for users.

## Specific Task Notes (If any)

-   If tasks involve changing LLM prompts (in `text_processor.py`), test thoroughly to ensure desired output quality.
-   If modifying dependencies, especially major ones like `openai-whisper` or `ollama`, be aware of potential impacts on resource usage or setup complexity.

Good luck!
```
