from django.db import models
import math
import googlemaps
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import requests

# Consider using choices for fields like managed_by, institute, status
# for better data consistency.

class Accommodation(models.Model):

    room_number = models.PositiveIntegerField(null=True, blank=True) # Assuming room number is numeric, nullable
    flat_number = models.CharField(max_length=10) # e.g., '1', 'C', '(null)' -> store as string
    floor_number = models.PositiveIntegerField()
    building_name = models.CharField(max_length=100)
    availability_start = models.DateField()
    availability_end = models.DateField()
    number_of_beds = models.PositiveIntegerField(default=1) # Default to 1 bed
    no_of_bedrooms = models.PositiveIntegerField(default=1) # Default to 1 bedroom
    type_of_accommodation = models.CharField(max_length=50) # e.g., 'Single', 'Double', 'Shared'
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2) # Assuming price is in HKD
    managed_by = models.CharField(max_length=100) # Could be ForeignKey if manager is complex
    latitude = models.FloatField(blank=True, null=True) # Nullable for existing records
    longitude = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUcampus = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUcampus_sassoon = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUcampus_swire = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUcampus_kadoorie = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUcampus_dentistry = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_CUHKcampus = models.FloatField(blank=True, null=True) # Nullable for existing records
    distance_to_HKUSTcampus = models.FloatField(blank=True, null=True) # Nullable for existing records
    active = models.BooleanField(default=True) # To mark if the accommodation is active or not

    def save(self, *args, **kwargs):
        gmaps = googlemaps.Client(key="AIzaSyDNdW_654A2GV7tiNtQtvpClz10WM9D5zs")
        geocode_result = gmaps.geocode(self.building_name)
        campus_HKU_latitude = 22.2830891
        campus_HKU_longitude = 114.1365621

        campus_HKU_sassoon_latitude =  22.2675
        campus_HKU_sassoon_longitude = 114.12881

        campus_HKU_swire_latitude = 22.20805
        campus_HKU_swire_longitude = 114.26021

        campus_HKU_dentistry_latitude = 22.28649
        campus_HKU_dentistry_longitude = 114.14426

        campus_HKU_kadoorie_latitude = 22.43022
        campus_HKU_kadoorie_longitude = 114.11429

        campus_CUHK_latitude = 22.396428
        campus_CUHK_longitude = 114.200203

        campus_HKUST_latitude = 22.335
        campus_HKUST_longitude = 114.265

        def get_lat_long(address):
            address += " Hong Kong"  # Append "Hong Kong" to the address for better geocoding
            url = "https://geodata.gov.hk/gs/api/v1/locationSearch?q=" + requests.utils.quote(address)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    first_result = data["results"][0]
                    lat = first_result.get("y")  # Assuming 'y' is latitude
                    lon = first_result.get("x")  # Assuming 'x' is longitude
                    if lat is not None and lon is not None:
                        return lat, lon
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
        self.distance_to_HKUcampus = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKU_latitude, campus_HKU_longitude)))
        self.distance_to_HKUcampus_sassoon = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKU_sassoon_latitude, campus_HKU_sassoon_longitude)))
        self.distance_to_HKUcampus_kadoorie = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKU_kadoorie_latitude, campus_HKU_kadoorie_longitude)))
        self.distance_to_CUHKcampus = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_CUHK_latitude, campus_CUHK_longitude)))
        self.distance_to_HKUSTcampus = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKUST_latitude, campus_HKUST_longitude)))
        self.distance_to_HKUcampus_swire = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKU_swire_latitude, campus_HKU_swire_longitude)))
        self.distance_to_HKUcampus_dentistry = float('{:.4g}'.format(haversine(self.latitude, self.longitude, campus_HKU_dentistry_latitude, campus_HKU_dentistry_longitude)))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.building_name} - Floor {self.floor_number}, Flat {self.flat_number}" + (f", Room {self.room_number}" if self.room_number else "")

class Member(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20) # Assuming contact is unique phone number
    institute = models.CharField(max_length=50) # e.g., HKU, CUHK
    email = models.EmailField(max_length=100) # Assuming email is unique
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

    # Store the original active status to detect changes
    _original_active = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the initial active status when the object is loaded
        self._original_active = self.active

    def clean(self):
        """
        Custom validation to prevent setting active=False when status is 'Signed'.
        Also prevents overlapping reservations for the same accommodation.
        """
        super().clean() # Call parent clean first

        # Validation 1: Prevent inactive status for signed contracts
        if self.status == 'Signed' and not self.active:
            raise ValidationError("A reservation with a signed contract cannot be set to inactive.")

        # Validation 2: Prevent date inconsistencies
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date cannot be before start date.")

        # Validation 3: Prevent overlapping reservations for the same accommodation
        if self.accommodation and self.start_date and self.end_date:
            overlapping_reservations = Reservation.objects.filter(
                accommodation=self.accommodation,
                start_date__lt=self.end_date, # Existing starts before new ends
                end_date__gt=self.start_date, # Existing ends after new starts
                active=True # Only consider active reservations for overlap check
            )
            # Exclude self if updating an existing reservation
            if self.pk:
                overlapping_reservations = overlapping_reservations.exclude(pk=self.pk)

            if overlapping_reservations.exists():
                raise ValidationError(
                    f"This accommodation is already reserved during the period {self.start_date} to {self.end_date}."
                )


    def save(self, *args, **kwargs):
        """
        Ensure clean() is called before saving.
        Send email notification if active status changes.
        """
        self.full_clean() # Use full_clean to run all model validations including clean()

        # Check if the active status has changed
        send_email_notification = False
        if self.pk is not None: # Check if this is an update
            # Fetch the original object from the database if not already stored
            if self._original_active is None:
                try:
                    original = Reservation.objects.get(pk=self.pk)
                    self._original_active = original.active
                except Reservation.DoesNotExist:
                    # Handle case where the object doesn't exist yet (shouldn't happen in save update)
                    pass # Or log an error

            if self._original_active != self.active:
                send_email_notification = True

        super().save(*args, **kwargs) # Save the object first

        # Send email after saving if status changed
        if send_email_notification:
            subject = 'Your Reservation Status Has Changed'
            new_status = "Active" if self.active else "Inactive"
            message = (
                f"Dear {self.member.name},\n\n"
                f"The status of your reservation for {self.accommodation} "
                f"from {self.start_date} to {self.end_date} has been updated to: {new_status}.\n\n"
                f"Thank you,\nUniHaven Team"
            )
            recipient_list = [self.member.email]
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
                # Update the stored original status after successful save and email
                self._original_active = self.active
            except Exception as e:
                # Handle email sending errors (e.g., log the error)
                print(f"Error sending email notification for reservation {self.pk}: {e}")
                # Optionally, decide if the save should be rolled back or if the error is acceptable


    def __str__(self):
        return f"Reservation for {self.accommodation} by {self.member} ({self.start_date} to {self.end_date})"

    class Meta:
        # Ordering can be useful
        ordering = ['accommodation', 'start_date']
        # The UniqueConstraint might be too strict if you allow multiple members
        # to reserve the exact same dates (unlikely but possible).
        # The clean method provides more flexible overlap checking.
        # constraints = [
        #     models.UniqueConstraint(fields=['accommodation', 'start_date', 'end_date'], name='unique_reservation_dates')
        # ]




from django.utils import timezone # Import timezone

class Rating(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='ratings')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()  # Assuming a rating scale of 1-5
    comment = models.TextField(null=True, blank=True)  # Optional comment
    active = models.BooleanField(default=True)  # To mark if the rating is active or not

    def clean(self):
        """
        Validate that the member can only rate the accommodation after
        their reservation period for it has ended.
        """
        super().clean() # Call parent clean first

        if self.member and self.accommodation:
            # Check if there is any completed reservation for this member and accommodation
            completed_reservations = Reservation.objects.filter(
                member=self.member,
                accommodation=self.accommodation,
                end_date__lt=timezone.now().date(), # Check if reservation end date is in the past
                active=True # Optionally, consider only active/signed reservations
                # status='Signed' # Uncomment if only signed contracts allow rating
            )

            if not completed_reservations.exists():
                raise ValidationError(
                    "You can only rate an accommodation after your reservation period has ended."
                )

        # Validate rating value (e.g., between 1 and 5)
        if self.rating is not None and not (1 <= self.rating <= 5):
             raise ValidationError("Rating must be between 1 and 5.")


    def save(self, *args, **kwargs):
        """
        Ensure clean() is called before saving.
        """
        self.full_clean() # Run model validation including the custom clean method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rating for {self.accommodation} by {self.member}: {self.rating}"

    class Meta:
        # Prevent multiple ratings by the same member for the same accommodation
        unique_together = ('accommodation', 'member')
        ordering = ['-rating', '-pk'] # Order by rating descending, then by pk descending
