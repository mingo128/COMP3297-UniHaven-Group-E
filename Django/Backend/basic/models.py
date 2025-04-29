from django.db import models

# Consider using choices for fields like managed_by, institute, status
# for better data consistency.

class Accommodation(models.Model):
    room_number = models.PositiveIntegerField(null=True, blank=True) # Assuming room number is numeric, nullable
    flat_number = models.CharField(max_length=10) # e.g., '1', 'C', '(null)' -> store as string
    floor_number = models.PositiveIntegerField()
    building_name = models.CharField(max_length=100)
    availability_start = models.DateField()
    availability_end = models.DateField()
    managed_by = models.CharField(max_length=100) # Could be ForeignKey if manager is complex

    def __str__(self):
        return f"{self.building_name} - Floor {self.floor_number}, Flat {self.flat_number}" + (f", Room {self.room_number}" if self.room_number else "")

class Member(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, unique=True) # Assuming contact is unique phone number
    institute = models.CharField(max_length=50) # e.g., HKU, CUHK

    def __str__(self):
        return f"{self.name} ({self.institute})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Signed', 'Contract Signed'),
        ('Not Signed', 'Contract Not signed'),
    ]

    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Reservation for {self.accommodation} by {self.member} ({self.start_date} to {self.end_date})"

    class Meta:
        # Optional: Add constraints, e.g., prevent overlapping reservations for the same accommodation
        constraints = [
            models.UniqueConstraint(fields=['accommodation', 'start_date', 'end_date'], name='unique_reservation_dates')
        ]
    



class Rating(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='ratings')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()  # Assuming a rating scale of 1-5
    comment = models.TextField(null=True, blank=True)  # Optional comment

    def __str__(self):
        return f"Rating for {self.accommodation} by {self.member}: {self.rating}"
    class Meta:
        unique_together = ('accommodation', 'member')
        # Prevent multiple ratings by the same member for the same accommodation
        ordering = ['-rating']
