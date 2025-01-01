import subprocess
from django.core.management.base import BaseCommand
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
    ],
)

class Command(BaseCommand):
    help = "Trigger Scrapy spider from Django"

    def handle(self, *args, **kwargs):
        container_name = "scrapy_container"  # Name of the Scrapy container
        spider_name = "llm_scrapy"  # Name of the spider to run

        self.stdout.write(f"Running Scrapy spider '{spider_name}' in container '{container_name}'")

        try:
            # Execute the Scrapy spider using `docker exec`
            result = subprocess.run(
                ["docker", "exec", container_name, "scrapy", "crawl", spider_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Log and print the success output
            logging.info(f"Scrapy spider '{spider_name}' ran successfully.")
            self.stdout.write(self.style.SUCCESS(result.stdout))

        except subprocess.CalledProcessError as e:
            # Log and print the error
            error_message = f"Failed to run Scrapy spider '{spider_name}': {e.stderr.strip()}"
            logging.error(error_message)
            self.stderr.write(self.style.ERROR(error_message))
