import os
from django.db import models

class Hotel(models.Model):
    property_ID = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    rating = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image_urls = models.TextField(null=True, blank=True)
    url = models.URLField()

    class Meta:
        db_table = "hotels"  # Match the table name in the Scrapy database

    def __str__(self):
        return self.title


class GeneratedSummary(models.Model):
    property_id = models.CharField(max_length=255)  # Store the property_ID as a string
    summary = models.TextField()

    class Meta:
        db_table = "generated_summary"

    def __str__(self):
        return f"Summary for property ID {self.property_id}"


class GeneratedReview(models.Model):
    property_id = models.CharField(max_length=255)  # Store the property_ID as a string
    rating = models.FloatField()  # Rating out of 10
    review = models.TextField()  # Fake review content

    class Meta:
        db_table = "generated_review"

    def __str__(self):
        return f"Review for property ID {self.property_id} with rating {self.rating}"
