import requests
import json

class TeamsPoster:
    def __init__(self, webhook_url):
        if not webhook_url:
            raise ValueError("MS Teams Webhook URL cannot be empty.")
        if not webhook_url.startswith("https://"):
            # Basic validation, actual Teams URLs have a more specific format
            print("Warning: The provided webhook URL seems invalid. Ensure it's a correct MS Teams Incoming Webhook URL.")
        self.webhook_url = webhook_url

    def post_message(self, title, message_text):
        """
        Posts a message to MS Teams using an Incoming Webhook.
        The message is formatted as a simple card.
        """
        if not message_text or message_text.isspace():
            print("Message text is empty. Nothing to post to Teams.")
            return False

        headers = {"Content-Type": "application/json"}

        # Basic adaptive card format for better presentation
        # For more complex cards, refer to MS Teams Adaptive Card documentation
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None, # Important for adaptive cards
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4", # Or a version you prefer
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": title,
                                "weight": "bolder",
                                "size": "medium"
                            },
                            {
                                "type": "TextBlock",
                                "text": message_text,
                                "wrap": True
                            }
                        ]
                    }
                }
            ]
        }

        print(f"\nPosting message to MS Teams...")
        try:
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

            if response.status_code == 200 or response.text == "1": # Teams webhook sometimes returns "1" for success
                print("Message posted successfully to MS Teams.")
                return True
            else:
                # This case might not be reached if raise_for_status() catches it
                print(f"Failed to post message to MS Teams. Status: {response.status_code}, Response: {response.text}")
                return False
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error posting to MS Teams: {e}")
            print(f"Response content: {e.response.content.decode() if e.response else 'No response content'}")
        except requests.exceptions.RequestException as e:
            print(f"Error posting to MS Teams: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while posting to Teams: {e}")
        return False

if __name__ == '__main__':
    # This is a test that requires a real MS Teams Webhook URL.
    # Set the MS_TEAMS_WEBHOOK_URL environment variable for testing.
    import os
    from dotenv import load_dotenv

    load_dotenv() # Loads variables from .env file into environment variables

    webhook_url_env = os.getenv("MS_TEAMS_WEBHOOK_URL")

    if not webhook_url_env:
        print("MS_TEAMS_WEBHOOK_URL not found in environment variables or .env file.")
        print("To test, please set it. Example .env file content:")
        print("MS_TEAMS_WEBHOOK_URL='your_webhook_url_here'")
    else:
        print(f"Using webhook URL from environment: {webhook_url_env[:50]}...") # Print part of it for confirmation
        try:
            poster = TeamsPoster(webhook_url=webhook_url_env)

            title = "Test: Action Items from Audio Processor"
            action_items_test = """
- Item 1: Review the quarterly report.
- Item 2: Schedule a follow-up meeting for next week.
- Item 3: Update the project documentation.
            """

            success = poster.post_message(title, action_items_test)
            if success:
                print("Test message sent. Check your MS Teams channel.")
            else:
                print("Test message failed to send.")

        except ValueError as ve:
            print(f"Error initializing TeamsPoster: {ve}")
        except Exception as e:
            print(f"An error occurred during the test: {e}")

    print("\nGuidance: How to create an Incoming Webhook in MS Teams:")
    print("1. Go to the desired channel in MS Teams.")
    print("2. Click on the three dots (...) for 'More options'.")
    print("3. Select 'Connectors'.")
    print("4. Search for 'Incoming Webhook' and click 'Configure' or 'Add'.")
    print("5. Provide a name for the webhook (e.g., 'AudioProcessorApp').")
    print("6. Click 'Create'.")
    print("7. Copy the generated Webhook URL. This is what you'll use in the application (e.g., in your .env file).")
    print("8. Click 'Done'.")
