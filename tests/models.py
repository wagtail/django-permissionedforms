from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Country(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        permissions = [
            ("change_country_description", "Can change country descriptions")
        ]


class Page(ClusterableModel):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    class Meta:
        permissions = [
            ("change_page_title", "Can change page titles")
        ]


class PageTag(models.Model):
    page = ParentalKey(Page, related_name='tags')
    tag = models.CharField(max_length=255)
