from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        permissions = [
            ("change_country_description", "Can change country descriptions")
        ]
