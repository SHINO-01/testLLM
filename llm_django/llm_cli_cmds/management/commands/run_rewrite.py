import os
import re
import requests
import time
import logging
from django.core.management.base import BaseCommand
from llm_cli_cmds.models import Hotel
from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
        logging.FileHandler("run_rewrite.log"),  # Logs to file
    ],
)

class Command(BaseCommand):
    help = "Rewrite hotel data using the Gemini API"

    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def call_gemini(self, text):
        """Call the Gemini API to generate rewritten content."""
        api_key = config("GEMINI_API_KEY")
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"parts": [{"text": text}]}
            ]
        }

        try:
            response = requests.post(
                f"{self.GEMINI_API_URL}?key={api_key}",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            logging.debug(f"Gemini API Response: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Gemini API request failed: {e}")
            return None

    def extract_title_and_description(self, api_response):
        """Extract title and description from the API response."""
        try:
            candidates = api_response.get("candidates", [])
            if candidates:
                text = candidates[0]["content"]["parts"][0]["text"]
                # Assuming title is the first line and description follows
                lines = text.split("\n", 1)
                if len(lines) == 2:
                    return lines[0].strip(), lines[1].strip()
        except (KeyError, IndexError):
            logging.warning("Failed to extract title and description from response.")
        return None, None

    def clean_text(self, text):
        """Clean and normalize text for consistent formatting."""
        if text:
            # Remove specific prefixes and surrounding stars
            text = re.sub(r"(\*\*Description:\*\*|Description:|\*\*Title:\*\*|Title:|\*\*|\*)", "", text)
            text = text.strip()  # Remove leading/trailing whitespace
            text = text.replace("\n", " ")  # Replace newlines with spaces
            text = " ".join(text.split())  # Ensure single spaces
        return text

    def handle(self, *args, **kwargs):
        # Fetch data from the Hotel table
        hotels = Hotel.objects.all()
        for hotel in hotels:
            logging.info(f"Processing hotel: {hotel.title}")

            # Prepare prompt for rewriting title and description
            prompt = f"Rewrite the following: Title: {hotel.title}, Description: {hotel.description}, you are to provide only a single response without providing any variations to the answer. The Description should be detail oriented, creative and at least 200 words while the Title should be eye catching."

            # Call the Gemini API for this hotel
            api_response = self.call_gemini(prompt)

            if api_response:
                # Extract title and description from the API response
                new_title, new_description = self.extract_title_and_description(api_response)

                if new_title and new_description:
                    hotel.title = self.clean_text(new_title)
                    hotel.description = self.clean_text(new_description)
                    hotel.save()
                    logging.info(f"Successfully updated hotel: {hotel.title}")
                else:
                    logging.warning(f"Failed to update hotel {hotel.title}: Invalid response format.")

            # Add a delay before sending the next request
            time.sleep(2)
