from rest_framework import serializers
from .models import Bird, UserBird, Capture

class BirdSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Bird
        fields = ['id', 'name', 'label', 'icon_url']

    def get_icon_url(self, obj):
        if obj.icon:
            return self.context['request'].build_absolute_uri(obj.icon.url)
        return None



class CaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id', 'user_bird', 'image', 'confidence', 'ai_fact', 'captured_at']

class UserBirdSerializer(serializers.ModelSerializer):
    captures = CaptureSerializer(many=True, read_only=True)

    class Meta:
        model = UserBird
        fields = ['id', 'user', 'bird', 'unlocked', 'times_captured', 'first_captured_at', 'captures']
