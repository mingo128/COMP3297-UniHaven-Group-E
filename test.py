
from db import initialize_db
from method.cedars import (
    add_landlord, add_student, add_accommodation,
    get_accommodation, get_accommodation_details,
    delete_accommodation, delete_landlord, delete_student,
    get_all_landlords, delete_review)
from method.students import (
    apply_for_accommodation, get_my_applications,
    cancel_application, add_review
)
import datetime

def print_section(title):
    print("\n" + "="*10 + f" {title} " + "="*10)

def main():
    initialize_db()
    print_section("Database Initialized")

    # add landlord
    landlord_id = add_landlord("Mr. Chan", "chan@example.com", "12345678")
    print("Landlord ID:", landlord_id)

    # add student
    student_id = add_student("3036666666","Alice Wong", "alice@example.com", "87654321")
    print("Student ID:", student_id)

    # add accommodation
    # Example accommodation data
    now = datetime.datetime.now().isoformat()
    accommodation_data = {
        "type": "Apartment",
        "period_of_availability": "2025-06",
        "number_of_rooms_available": 3,
        "shared_bathroom": True,
        "price": 7800.0,
        "location": "Sheung Wan",
        "latitude": 22.287,
        "longitude": 114.150,
        "amenities": ["Wi-Fi", "Air-con"],
        "photos": ["image.png"],
        "landlord_id": landlord_id,
        "availability_calendar": [],
        "description": "Nice cozy apartment near MTR.",
        "created_at": now,
        "updated_at": now
    }

    acc_id = add_accommodation(accommodation_data)
    print("Accommodation ID:", acc_id)

    # list all accommodations
    print_section("Accommodation Listings")
    print(get_accommodation())

    # get accommodation details
    print_section("Accommodation Details")
    print(get_accommodation_details(acc_id))
    
    print(get_all_landlords())

    # student apply for accommodation
    print_section("Apply for Accommodation")
    app_id = apply_for_accommodation(student_id, acc_id, "I like this place.")
    print("Application ID:", app_id)

    # student get their applications
    print_section("My Applications")
    print(get_my_applications(student_id))

    # add review
    # Example review data
    print_section("Add Review")
    review_id = add_review(student_id, acc_id, {
        "overall_rating": 5,
        "value_for_money": 4,
        "location_convenience": 5,
        "property_condition": 4,
        "landlord_communication": 5,
        "review_text": "Great location and friendly landlord!",
        "photos": ["image.png"]
    })
    print("Review ID:", review_id)

    # student get their reviews
    print_section("Cancel Application")
    result = cancel_application(app_id)
    print("Cancelled:", result)

    # delete review
    print_section("Clean Up Reviews")
    print("Deleted review:", delete_review(review_id))
    
    ## delete accommodation
    print_section("Delete Accommodation")
    print("Deleted:", delete_accommodation(acc_id))


    ## delete landlord and student
    print_section("Delete Users")
    print("Delete student:", delete_student(student_id))
    print("Delete landlord:", delete_landlord(landlord_id))
    
    

if __name__ == "__main__":
    main()
