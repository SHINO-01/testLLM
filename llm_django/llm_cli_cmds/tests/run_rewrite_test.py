from unittest.mock import patch, Mock, MagicMock
from django.test import TestCase
from django.core.management import call_command
from llm_cli_cmds.management.commands.run_rewrite import Command
from llm_cli_cmds.models import Hotel, GeneratedSummary, GeneratedReview
import json

class TestRewriteCommand(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            property_ID="TEST123",
            title="Test Hotel",
            description="Test Description",
            location="Test Location"
        )
        
    @patch('llm_cli_cmds.management.commands.run_rewrite.requests.post')
    def test_call_gemini(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "New Title\nNew Description"}]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        command = Command()
        result = command.call_gemini("test text")
        
        self.assertIsNotNone(result)
        mock_post.assert_called_once()

    @patch('llm_cli_cmds.management.commands.run_rewrite.Command.call_gemini')
    def test_generate_summary(self, mock_call_gemini):
        mock_call_gemini.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Test Summary"}]
                }
            }]
        }
        
        command = Command()
        summary = command.generate_summary(self.hotel)
        
        self.assertEqual(summary, "Test Summary")
        mock_call_gemini.assert_called_once()

    @patch('llm_cli_cmds.management.commands.run_rewrite.Command.call_gemini')
    def test_generate_fake_review(self, mock_call_gemini):
        mock_call_gemini.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Review: Great hotel\nRating: 4.5"}]
                }
            }]
        }
        
        command = Command()
        rating, review = command.generate_fake_review(self.hotel)
        
        self.assertEqual(rating, 4.5)
        self.assertEqual(review, "Great hotel")
        mock_call_gemini.assert_called_once()

    @patch('llm_cli_cmds.management.commands.run_rewrite.Command.call_gemini')
    def test_handle_success(self, mock_call_gemini):
        mock_call_gemini.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "New Title\nNew Description"}]
                }
            }]
        }
        
        call_command('run_rewrite')
        
        # Verify hotel was updated
        updated_hotel = Hotel.objects.get(pk=self.hotel.pk)
        self.assertEqual(updated_hotel.title, "New Title")
        self.assertEqual(updated_hotel.description, "New Description")

    def test_clean_text(self):
        command = Command()
        test_text = "**Title:** Test **Description:** Test"
        cleaned_text = command.clean_text(test_text)
        self.assertEqual(cleaned_text, "Test Test")