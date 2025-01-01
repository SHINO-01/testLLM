import random
import re
import requests
import time
import logging
from django.core.management.base import BaseCommand
from llm_cli_cmds.models import Hotel, GeneratedSummary, GeneratedReview
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
    help = "Rewrite hotel data and generate summaries using the Gemini API"

    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

    def call_gemini(self, text):
        """Call the Gemini API to generate rewritten content or summaries."""
        api_key = config("GEMINI_API_KEY")
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"parts": [{"text": text}]}
            ]
        }

        retries = 3
        for attempt in range(retries):
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
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)  # Increase delay for retries
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
        except (KeyError, IndexError) as e:
            logging.warning(f"Error parsing API response: {e}")
        return "Unknown Title", "Unknown Description"

    def clean_text(self, text):
        """Clean and normalize text for consistent formatting."""
        if text:
            text = re.sub(r"(\*\*Description:\*\*|Description:|\*\*Title:\*\*|Title:|\*\*|\*)", "", text)
            text = text.strip()  # Remove leading/trailing whitespace
            text = re.sub(r"\s+", " ", text)  # Replace multiple spaces/newlines with a single space
        return text

    def generate_summary(self, hotel):
        """Generate a summary by passing title and description to the Gemini API."""
        prompt = f"Summarize the following description of hotels within 50 words: Title: {hotel.title}, Description: {hotel.description}"
        api_response = self.call_gemini(prompt)
        if api_response:
            try:
                candidates = api_response.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"].strip()
            except (KeyError, IndexError):
                logging.warning("Failed to extract summary from response.")
        return None

    def generate_fake_review(self, hotel):
        """Generate a fake review and rating for the hotel."""
        prompt = (
            f"Write a fake review for the following hotel: "
            f"Title: {hotel.title}, Description: {hotel.description}, Location: {hotel.location}. "
            f"Ensure the review is professional, realistic, and short. Also, make sure the rating is between 1 to 5 and can have a floating value. "
            f"Your response should follow the format: 'Review:' followed by the review text, and then 'Rating:' followed by the rating."
        )
        api_response = self.call_gemini(prompt)
        if api_response:
            try:
                candidates = api_response.get("candidates", [])
                if candidates:
                # Extract the full response text
                    response_text = candidates[0]["content"]["parts"][0]["text"].strip()
                
                # Use regex to extract the review and rating
                    review_match = re.search(r"Review:\s*(.+?)(?:\s*Rating:|$)", response_text, re.DOTALL)
                    rating_match = re.search(r"Rating:\s*([\d.]+)", response_text)
                
                    if review_match and rating_match:
                        review_text = review_match.group(1).strip()
                        rating = float(rating_match.group(1))
                        return rating, review_text
                    else:
                        logging.warning(f"Failed to parse review or rating from API response: {response_text}")
            except (KeyError, IndexError, ValueError) as e:
                logging.warning(f"Error parsing API response: {e}")
        return None, None

    def handle(self, *args, **kwargs):
        hotels = Hotel.objects.all()
        for hotel in hotels:
            logging.info(f"Processing hotel: {hotel.title}")

            # Prepare prompt for rewriting title and description
            prompt = f"Rewrite the following: Title: {hotel.title}, Description: {hotel.description}, you are to provide only a single response without providing any variations to the answer. The Description should be detail oriented and the Title should be eye-catching."

            api_response = self.call_gemini(prompt)

            if api_response:
                new_title, new_description = self.extract_title_and_description(api_response)

                hotel.title = self.clean_text(new_title)
                hotel.description = self.clean_text(new_description)
                hotel.save()
                logging.info(f"Updated hotel: {hotel.title}")
                
                time.sleep(1)

                summary = self.generate_summary(hotel)
                if summary:
                    GeneratedSummary.objects.create(property_id=hotel.property_ID, summary=summary)
                    logging.info(f"Saved summary for hotel: {hotel.title}")
                
                time.sleep(1)

                rating, review = self.generate_fake_review(hotel)
                if rating and review:
                    GeneratedReview.objects.create(
                        property_id=hotel.property_ID,
                        rating=rating,
                        review=review
                    )
                    logging.info(f"Saved fake review for hotel: {hotel.title}")
            time.sleep(3)  # Add delay between requests
