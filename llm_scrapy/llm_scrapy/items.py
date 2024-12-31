import scrapy

class HotelScrapperItem(scrapy.Item):
    city = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()  # Now stores downloaded image paths
    image_urls = scrapy.Field()  # Field for Scrapy's ImagesPipeline
    url = scrapy.Field()