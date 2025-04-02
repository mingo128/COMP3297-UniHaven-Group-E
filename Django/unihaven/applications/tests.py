import uuid
from datetime import date
import pytest
from .models import Application

class DummyUser:
    def get_full_name(self):
        return "John Doe"


class DummyAccommodation:
    type = "Apartment"


@pytest.mark.django_db
def test_application_str():
    # Create dummy objects for foreign keys
    dummy_user = DummyUser()
    dummy_accommodation = DummyAccommodation()

    # Instantiate Application without saving to DB
    app_instance = Application(
        accommodation=dummy_accommodation,
        user=dummy_user,
        status='pending',
        rental_contract_start_date=date(2023, 1, 1),
        rental_contract_end_date=date(2023, 12, 31),
        notes="Test note"
    )
    # Force model field defaults and validations (including auto-generated UUID)
    app_instance.full_clean()

    expected = f"Application {app_instance.id} by John Doe for Apartment"
    assert str(app_instance) == expected