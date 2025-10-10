from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bird, UserBird, Capture
from .serializers import CaptureSerializer, UserBirdSerializer
from django.contrib.auth.models import User
from utils.ml_client import classify_bird  

class CaptureBirdView(APIView):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ Send image to FastAPI model
        prediction = classify_bird(image_file)
        if not prediction:
            return Response({"error": "ML service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        predicted_label = prediction["label"]
        confidence = prediction["confidence"]

        # 2️⃣ Find the bird
        try:
            bird = Bird.objects.get(label=predicted_label)
        except Bird.DoesNotExist:
            return Response({"error": f"Bird '{predicted_label}' not found"}, status=status.HTTP_404_NOT_FOUND)

        # 3️⃣ Update or create UserBird
        user_bird, created = UserBird.objects.get_or_create(user=user, bird=bird)
        if not created:
            user_bird.times_captured += 1
        else:
            user_bird.unlocked = True
        user_bird.save()

        # 4️⃣ AI fun fact (placeholder)
        ai_fact = f"This is a {bird.name}! They’re known for their {bird.habitat or 'unique song'}."

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
            "confidence": confidence,
            "icon_url": bird.icon.url,
            "ai_fact": ai_fact,
        }, status=status.HTTP_201_CREATED)
