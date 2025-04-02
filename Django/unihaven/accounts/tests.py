from django.test import TestCase
from .models import User  # Assuming User model is defined in accounts/models.py

class UserModelTests(TestCase):

    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create(
            student_id='12345678',
            name='Test User',
            email='testuser@example.com',
            phone='1234567890'
        )

    def test_user_creation(self):
        """Test that a user can be created successfully."""
        self.assertEqual(self.user.student_id, '12345678')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone, '1234567890')

    def test_user_str(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), 'Test User')  # Assuming __str__ method returns the user's name

    def test_user_email(self):
        """Test that the email field is valid."""
        self.assertTrue('@' in self.user.email)  # Basic email validation check

    def test_user_phone(self):
        """Test that the phone number is valid."""
        self.assertTrue(self.user.phone.isdigit())  # Check if phone number contains only digits