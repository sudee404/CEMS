from django.db import models

# Create your models here.

class Event(models.Model):
	"""Model definition for Event."""

	title = models.CharField(max_length=50)
	description = models.TextField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	guests = models.PositiveIntegerField()
	poster = models.ImageField(upload_to='poster', height_field=1400, width_field=700, max_length=800)


	class Meta:
		"""Meta definition for Event."""

		verbose_name = 'Event'
		verbose_name_plural = 'Events'

	def __str__(self):
		"""Unicode representation of Event."""
		self.title
