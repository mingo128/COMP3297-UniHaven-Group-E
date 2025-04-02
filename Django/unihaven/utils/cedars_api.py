from django.conf import settings
import requests

def authenticate_user(student_id, password):
    url = f"{settings.CEDARS_API_URL}/authenticate"
    payload = {
        "student_id": student_id,
        "password": password
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()  # Return user data if authentication is successful
    else:
        return None  # Return None if authentication fails

def get_user_details(token):
    url = f"{settings.CEDARS_API_URL}/user/details"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return user details if the request is successful
    else:
        return None  # Return None if the request fails

def validate_student_id(student_id):
    url = f"{settings.CEDARS_API_URL}/validate_student_id"
    payload = {
        "student_id": student_id
    }
    response = requests.post(url, json=payload)
    
    return response.status_code == 200  # Return True if valid, False otherwise