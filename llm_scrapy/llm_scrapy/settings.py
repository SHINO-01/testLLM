import os

BOT_NAME = "llm_scrapy"

SPIDER_MODULES = ["llm_scrapy.spiders"]
NEWSPIDER_MODULE = "llm_scrapy.spiders"

ROBOTSTXT_OBEY = False  # Temporarily disabled for debugging
DOWNLOAD_DELAY = 1  # Reduced delay

# Configure the Images Pipeline
ITEM_PIPELINES = {
    "llm_scrapy.pipelines.HotelScrapperPipeline": 300,
}

# Handle HTTP error codes
HTTPERROR_ALLOW_ALL = True

# Logging configuration
LOG_LEVEL = 'DEBUG'
FEED_EXPORT_ENCODING = "utf-8"

# User-Agent to mimic a browser
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Retry configuration
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 404]

DATABASE = {
    'drivername': 'postgresql',
    'host': 'llm_db_cont',
    'port': '5432',
    'username': 'shino',
    'password': 'shinopass123',
    'database': 'llm_test_DB',
}