from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Represents one bird species in your BirdDex
class Bird(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100, unique=True)  # e.g. "northern_cardinal"
    icon = models.ImageField(upload_to="bird_icons/")  # pre-made static icon
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Tracks user ↔ bird relationship (unlocked or not)
class UserBird(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # null for anonymous MUST CHANGE LATER!!!!!!!!!!
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    first_captured_at = models.DateTimeField(auto_now_add=True)
    times_captured = models.PositiveIntegerField(default=1)
    unlocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'bird')

    def __str__(self):
        return f"{self.user.username} - {self.bird.name}"


# Stores each individual bird photo a user takes
class Capture(models.Model):
    user_bird = models.ForeignKey(UserBird, on_delete=models.CASCADE, related_name='captures')
    image = models.ImageField(upload_to='captures/')
    confidence = models.FloatField()
    ai_fact = models.TextField(null=True, blank=True)  # AI-generated fun fact
    model_version = models.CharField(max_length=50, default='v1.0')  # for ML tracking
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_bird.user.username} - {self.user_bird.bird.name} ({self.confidence:.2f})"
