from unittest.mock import patch, Mock
from django.test import TestCase
from django.core.management import call_command
from llm_cli_cmds.management.commands.run_scrapy import Command
import subprocess

class TestScrapyCommand(TestCase):
    @patch('subprocess.run')
    def test_handle_success(self, mock_run):
        mock_result = Mock()
        mock_result.stdout = "Spider finished successfully"
        mock_result.check = True
        mock_run.return_value = mock_result
        
        call_command('run_scrapy')
        
        mock_run.assert_called_once_with(
            ["docker", "exec", "scrapy_container", "scrapy", "crawl", "llm_scrapy"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    @patch('subprocess.run')
    def test_handle_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            1, 'cmd', stdout="", stderr="Spider failed"
        )
        
        with self.assertLogs() as logs:
            call_command('run_scrapy')
            
        self.assertIn("ERROR", logs.output[0])