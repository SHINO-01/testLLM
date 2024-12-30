import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run the Scrapy spider"

    def handle(self, *args, **options):
        # Set the path to Scrapy project directory
        scrapy_project_path = "/app"  # Path inside the Scrapy container

        # Command to run the Scrapy spider
        spider_name = "hotel_spider"  # Replace with your spider's name
        command = ["scrapy", "crawl", spider_name]

        try:
            # Run the Scrapy spider
            self.stdout.write(f"Running spider: {spider_name} in {scrapy_project_path}")
            result = subprocess.run(
                command,
                cwd=scrapy_project_path,  # Use the correct Scrapy project path
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.stdout.write(self.style.SUCCESS(result.stdout))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Error running spider: {e.stderr}"))
