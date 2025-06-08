from django.db import models


class Anime(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.ImageField(
        upload_to='anime_images/',
        blank=True,
        null=True
        )
    trailer_url = models.URLField(blank=True, null=True)
    studio = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    episodes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=[
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
        ('cancelled', 'Cancelled'),
    ], default='ongoing')
    classification = models.CharField(max_length=50, choices=[
        ('tv', 'TV'),
        ('movie', 'Movie'),
        ('ova', 'OVA'),
        ('ona', 'ONA'),
        ('special', 'Special'),
        ('tv_short', 'TV Short'),
    ], default='tv')
    classification_detail = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )

    def __str__(self):
        return self.title
