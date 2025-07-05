import ollama
import os

class TextProcessor:
    def __init__(self, ollama_model_name="llama2", ollama_host=None):
        self.ollama_model_name = ollama_model_name
        self.client = ollama.Client(host=ollama_host) if ollama_host else ollama.Client()
        print(f"Ollama client for text processing initialized. Model: {self.ollama_model_name}, Target host: {self.client._client.base_url}")
        try:
            self.client.show(self.ollama_model_name)
            print(f"Successfully connected to Ollama and model '{self.ollama_model_name}' is available.")
        except ollama.ResponseError as e:
            print(f"Warning: Ollama model '{self.ollama_model_name}' not found or error connecting: {e}")
            print("Summarization and action item generation may fail if the model is not available.")


    def summarize_text(self, text, max_length=150): # max_length is indicative
        if not text or text.isspace():
            return "Error: Input text is empty, cannot summarize."
        print(f"\nSummarizing text using Ollama model {self.ollama_model_name}...")

        prompt = f"""Summarize the following text in about 3-4 key sentences:

{text}

Summary:"""

        try:
            response = self.client.chat(
                model=self.ollama_model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            summary = response['message']['content']
            print("Summarization complete.")
            return summary.strip()
        except ollama.ResponseError as e:
            error_msg = f"Error during summarization with Ollama: {e.status_code} - {e.error}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"An unexpected error occurred during summarization: {e}"
            print(error_msg)
            return error_msg

    def generate_action_items(self, text):
        if not text or text.isspace():
            return "Error: Input text is empty, cannot generate action items."
        print(f"\nGenerating action items using Ollama model {self.ollama_model_name}...")

        prompt = f"""Based on the following text, extract key action items.
If no specific action items are mentioned, state 'No specific action items found'.
Present the action items as a bulleted list.

Text:
{text}

Action Items:"""

        try:
            response = self.client.chat(
                model=self.ollama_model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            action_items = response['message']['content']
            print("Action item generation complete.")
            return action_items.strip()
        except ollama.ResponseError as e:
            error_msg = f"Error during action item generation with Ollama: {e.status_code} - {e.error}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"An unexpected error occurred during action item generation: {e}"
            print(error_msg)
            return error_msg

if __name__ == '__main__':
    ollama_host = os.getenv("OLLAMA_HOST")
    # Ensure you have a model like 'llama2' or 'mistral' pulled in your Ollama.
    processor = TextProcessor(ollama_model_name="llama2", ollama_host=ollama_host)

    sample_text_meeting = """
    Alright team, good meeting. So, to recap:
    John, you're going to investigate the new CRM software options and report back by next Friday.
    Sarah, please finalize the Q3 budget proposal and send it to me by end of day Wednesday.
    Mike, can you look into the customer complaints from last week regarding the login issue? We need a fix ASAP.
    And I will draft the agenda for the client presentation.
    Any questions? No? Great.
    Oh, and everyone remember to submit your timesheets by tomorrow.
    """

    sample_text_general = "The weather is sunny today. It's a good day for a walk in the park. Many people are enjoying the outdoors."

    print("\n--- Testing with Meeting Transcript ---")
    if "Warning:" not in processor.summarize_text("test"): # Quick check if model is likely available
        summary = processor.summarize_text(sample_text_meeting)
        print("\nSummary:")
        print(summary)

        action_items = processor.generate_action_items(sample_text_meeting)
        print("\nAction Items:")
        print(action_items)
    else:
        print("Skipping Ollama processing tests as model connection seems to have issues.")

    print("\n--- Testing with General Text (expect no action items) ---")
    if "Warning:" not in processor.summarize_text("test"):
        summary_general = processor.summarize_text(sample_text_general)
        print("\nSummary (General Text):")
        print(summary_general)

        action_items_general = processor.generate_action_items(sample_text_general)
        print("\nAction Items (General Text):")
        print(action_items_general)
    else:
        print("Skipping Ollama processing tests as model connection seems to have issues.")
