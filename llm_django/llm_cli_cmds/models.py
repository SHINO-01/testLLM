from django.db import models

class Hotel(models.Model):
    property_ID = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255)
    title = models.CharField(max_length=255)  # Existing title field
    rating = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Existing description field
    price = models.FloatField(null=True, blank=True)
    image_urls = models.TextField(null=True, blank=True)  # Store image URLs as a comma-separated string
    url = models.URLField()

    class Meta:
        db_table = "hotels"  # Match the table name in the Scrapy database

    def __str__(self):
        return self.title
