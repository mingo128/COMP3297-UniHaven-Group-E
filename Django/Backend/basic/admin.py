from django.contrib import admin
from .models import Accommodation, Member, Reservation, Rating

# Register your models here to make them accessible in the Django admin interface
admin.site.register(Accommodation)
admin.site.register(Member)
admin.site.register(Reservation)
admin.site.register(Rating)