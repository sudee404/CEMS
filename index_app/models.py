from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Event(models.Model):
    """Model definition for Event."""
    category = models.ForeignKey(
        "Category", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    guests = models.PositiveIntegerField(null=True)
    poster = models.ImageField(
        upload_to='poster', default='default.png')
    draft = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        """Meta definition for Event."""

        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['start_date']

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"pk": self.pk})

    def __str__(self):
        """Unicode representation of Event."""
        return self.title


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='images', default='default.png')
    description = models.TextField()

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name
