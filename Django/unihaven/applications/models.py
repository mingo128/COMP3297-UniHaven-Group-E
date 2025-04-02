from django.db import models
from django.conf import settings
import uuid

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accommodation = models.ForeignKey('accommodations.Accommodation', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled'),
    ])
    rental_contract_start_date = models.DateField()
    rental_contract_end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Application {self.id} by {self.user.get_full_name()} for {self.accommodation.type}"