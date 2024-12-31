import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Trigger Scrapy spider from Django"

    def handle(self, *args, **kwargs):
        container_name = "scrapy_container"  # Name of the Scrapy container
        spider_name = "llm_scrapy"  # Name of the spider to run

        try:
            # Run Scrapy in its container using docker exec
            self.stdout.write(f"Running Scrapy spider '{spider_name}' in container '{container_name}'")
            result = subprocess.run(
                ["docker", "exec", container_name, "scrapy", "crawl", spider_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.stdout.write(self.style.SUCCESS(result.stdout))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Failed to run Scrapy: {e.stderr}"))
