from django.contrib import admin
from .models import Bird, UserBird, Capture

admin.site.register(Bird)
admin.site.register(UserBird)
admin.site.register(Capture)
