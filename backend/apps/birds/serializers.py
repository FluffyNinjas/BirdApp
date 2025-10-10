from rest_framework import serializers
from .models import Bird, UserBird, Capture

class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = ['id', 'name', 'label', 'icon']

class CaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id', 'user_bird', 'image', 'confidence', 'ai_fact', 'captured_at']

class UserBirdSerializer(serializers.ModelSerializer):
    captures = CaptureSerializer(many=True, read_only=True)

    class Meta:
        model = UserBird
        fields = ['id', 'user', 'bird', 'unlocked', 'times_captured', 'first_captured_at', 'captures']
