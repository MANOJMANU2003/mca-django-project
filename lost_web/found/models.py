from django.db import models

# Create your models here.

class userdetails(models.Model):
    username = models.CharField(max_length=100)
    userpw = models.CharField(max_length=100)

class Report(models.Model):
    REPORT_TYPES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=150)
    date = date = models.DateField()

    def __str__(self):
        return f"{self.report_type} - {self.item_name}"