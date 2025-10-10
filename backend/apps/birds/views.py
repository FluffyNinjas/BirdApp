# birds/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bird, UserBird, Capture
from .serializers import CaptureSerializer, UserBirdSerializer
from django.contrib.auth.models import User
from backend.utils.ml_client import classify_bird  
from backend.utils.ai_client import generate_bird_fact  # Stub for AI fun fact

class CaptureBirdView(APIView):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ Call the ML service
        predicted_label, confidence = classify_bird(image_file)

        if not predicted_label:
            return Response({"error": "Could not classify bird"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 2️⃣ Find the bird
        try:
            bird = Bird.objects.get(label=predicted_label)
        except Bird.DoesNotExist:
            return Response({"error": "Unknown bird species"}, status=status.HTTP_404_NOT_FOUND)

        # 3️⃣ Check if user already unlocked this bird
        user_bird, created = UserBird.objects.get_or_create(user=user, bird=bird)
        if not created:
            user_bird.times_captured += 1
            user_bird.save()
        else:
            user_bird.unlocked = True
            user_bird.save()

        # 4️⃣ Optionally call AI to generate fun fact (stub for now)
        ai_fact = generate_bird_fact(bird.name)

        # 5️⃣ Save capture
        capture = Capture.objects.create(
            user_bird=user_bird,
            image=image_file,
            confidence=confidence,
            ai_fact=ai_fact
        )

        return Response({
            "bird_name": bird.name,
            "first_time": created,
            "icon_url": bird.icon.url,
            "ai_fact": ai_fact,
        }, status=status.HTTP_201_CREATED)
