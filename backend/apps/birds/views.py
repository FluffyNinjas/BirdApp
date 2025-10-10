from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bird, UserBird, Capture
from .serializers import CaptureSerializer, UserBirdSerializer
from django.contrib.auth.models import User

class CaptureBirdView(APIView):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        image_file = request.FILES.get('image')

        # 1️⃣ Run your ML model here to predict the bird label
        predicted_label = "robin"  # example; replace with your ML call
        confidence = 0.92

        # 2️⃣ Find the bird
        bird = Bird.objects.get(label=predicted_label)

        # 3️⃣ Check if user already unlocked this bird
        user_bird, created = UserBird.objects.get_or_create(user=user, bird=bird)
        if not created:
            user_bird.times_captured += 1
            user_bird.save()
        else:
            user_bird.unlocked = True
            user_bird.save()

        # 4️⃣ Optionally call AI to generate fun fact
        ai_fact = f"This is a {bird.name}. Fun fact here!"  # replace with Gemini API call

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
