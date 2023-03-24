from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File

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
    host = models.ForeignKey(User(), on_delete=models.CASCADE,null=True)
    approved = models.BooleanField(default=False)
    draft = models.BooleanField(default=True)
    venue = models.ForeignKey('venue',on_delete=models.SET_NULL,null=True)


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


class Guest(models.Model):
    """Model definition for Guest."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.UUIDField(
        default=uuid.uuid4, help_text='Unique ID for this particular ticket')
    scanned = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr/')


    class Meta:
        """Meta definition for Guest."""

        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
        unique_together = ('user', 'event')
        ordering = ['-event__start_date']


    def __str__(self):
        """Unicode representation of Guest."""
        return self.user.username
    
    #  We overide the save function to create a qr image
    #  from the unique id assigned to every attendee object
    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(self.ticket)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        canvas = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        fname = f'{self.ticket}.png'
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
      
class Venue(models.Model):
    """Model definition for Venue."""

    name= models.CharField(max_length=250)
    description = models.TextField(blank=True)
    location = models.ForeignKey('Location',on_delete=models.SET_NULL,null=True)
    poster = models.ImageField(
        upload_to='poster', default='default.png')
    capacity = models.PositiveSmallIntegerField(default=30)
    
    class Meta:
        """Meta definition for Venue."""

        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'

    def __str__(self):
        """Unicode representation of Venue."""
        return self.name

class Location(models.Model):
    """Model definition for Location."""

    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

    def __str__(self):
        """Unicode representation of Location."""
        return self.city
        
    class Meta:
        """Meta definition for Location."""

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    
