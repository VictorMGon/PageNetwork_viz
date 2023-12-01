from django.db import models

# Create your models here.
class Page(models.Model):
    url = models.URLField()
    scrapped = models.BooleanField(default=False)
    date_scrapped = models.DateTimeField("date scrapped")

class Link(models.Model):
    source_page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name="Source")
    target_page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name="Target")