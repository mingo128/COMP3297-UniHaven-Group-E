from django.contrib import admin
from .models import User  # Assuming User is defined in models.py

admin.site.register(User)  # Register the User model with the admin site