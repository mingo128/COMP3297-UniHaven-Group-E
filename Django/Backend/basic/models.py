from django.db import models
import math
import googlemaps

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
    latitude = models.FloatField(blank=True, null=True) # Nullable for existing records
    longitude = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_campus = models.FloatField(blank=True, null=True) # Nullable for existing records
    active = models.BooleanField(default=True) # To mark if the accommodation is active or not

    def save(self, *args, **kwargs):
        gmaps = googlemaps.Client(key="AIzaSyDNdW_654A2GV7tiNtQtvpClz10WM9D5zs")
        geocode_result = gmaps.geocode(self.building_name)
        campus_latitude = 22.2830891
        campus_longitude = 114.1365621

        def get_lat_long(address):
            address += " Hong Kong"  # Append "Hong Kong" to the address for better geocoding
            # Use Google Maps API to get latitude and longitude
            geocode_result = gmaps.geocode(address)
            if geocode_result:
                lat = geocode_result[0]['geometry']['location']['lat']
                lon = geocode_result[0]['geometry']['location']['lng']
                return lat, lon
            else:
                raise ValueError("Could not find location for address: " + address)

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)
            a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c
                
        self.latitude, self.longitude = get_lat_long(self.building_name)
        self.distance_to_campus = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_latitude, campus_longitude)))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.building_name} - Floor {self.floor_number}, Flat {self.flat_number}" + (f", Room {self.room_number}" if self.room_number else "")

class Member(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, unique=True) # Assuming contact is unique phone number
    institute = models.CharField(max_length=50) # e.g., HKU, CUHK
    active = models.BooleanField(default=True) # To mark if the member is active or not

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
    active = models.BooleanField(default=True) # To mark if the reservation is active or not

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
    active = models.BooleanField(default=True)  # To mark if the rating is active or not

    def __str__(self):
        return f"Rating for {self.accommodation} by {self.member}: {self.rating}"
    class Meta:
        unique_together = ('accommodation', 'member')
        # Prevent multiple ratings by the same member for the same accommodation
        ordering = ['-rating']
