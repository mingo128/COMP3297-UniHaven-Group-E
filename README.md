# COMP3297-UniHaven-Group-E

This repository contains the code for the UniHaven Accommodation Management System, developed as part of the COMP3297 course at The University of Hong Kong.

## Update After Meeting

---

### Fully Complete the tests.py for API testing

The `tests.py` file has been updated to include comprehensive test cases for the serializers of the `Accommodation`, `Member`, `Reservation`, and `Rating` models. Each test class includes setup methods, field content validation, and serializer validation checks.

- All CRUD operations are covered.
- Each serializer is tested for expected fields and content.
- Validations for creating new instances are included. ( duplicated data will be rejected )

---

### Geocoding Process Enhancement

The geocoding mechanism for obtaining latitude and longitude from addresses has been updated.

-   **Previous Method:** Utilized the Google Maps Geocoding API.
-   **New Method:** Switched to the Hong Kong government's **GeoData API**.
    -   Uses the endpoint: `https://geodata.gov.hk/gs/api/v1/locationSearch?q=<encoded_address>`
    -   Parses latitude (`y`) and longitude (`x`) from the JSON response.
    -   Includes improved error handling to raise a `ValueError` if the location cannot be found.
-   **Benefit:** This change potentially simplifies the process and removes the dependency on a Google API key.

---

### `Accommodation` Model Updates

The `Accommodation` model has been enhanced to capture more detailed information and calculate distances to university campuses.

-   **New Fields Added:**
    -   `no_of_bedrooms`: Integer field for the number of bedrooms (default: `1`).
    -   `number_of_beds`: Integer field for the number of beds (default: `1`).
    -   `type_of_accommodation`: String field for the accommodation type (e.g., 'Single', 'Double', 'Shared').
    -   `price_per_month`: Decimal field for the monthly rental price (assumed HKD).
    -   Multiple distance fields (Decimal type) calculated automatically:
        -   `distance_to_HKUcampus`
        -   `distance_to_HKUcampus_swire`
        -   `distance_to_HKUcampus_dentistry`
        -   `distance_to_CUHKcampus`
        -   *(Potentially others based on implementation)*

-   **Campus Coordinates Used for Calculation:**
    -   HKU Main Campus: *(Coordinates assumed to be pre-existing)*
    -   HKU Swire Campus: Latitude `22.20805`, Longitude `114.26021`
    -   HKU Dentistry Campus: Latitude `22.28649`, Longitude `114.14426`
    -   CUHK Campus: *(Coordinates assumed to be pre-existing)*

-   **Updated `save()` Method:**
    -   Refactored to incorporate the new GeoData API for geocoding the address.
    -   Calculates distances to multiple specified university campuses using the Haversine formula upon saving.
    -   Stores the calculated distances in the respective fields.

---

### `Member` Model Updates

-   **New Field Added:**
    -   `email`: An `EmailField` for member communication.
-   **Constraint Change:**
    -   Removed the `unique=True` constraint from the `contact` field.

---

### `Reservation` Model Updates

Significant enhancements were made to add validation and notifications.

-   **Custom Validation Logic (`clean()` method):**
    -   Prevents marking a reservation with `signed=True` as inactive (`active=False`).
    -   Disallows overlapping reservation date ranges for the *same* accommodation.
    -   Ensures the `start_date` is not after the `end_date`.
-   **Email Notifications (`save()` method):**
    -   Sends an email notification when a reservation's `active` status changes.
    -   Uses a custom `__init__` method to track the original `active` status for detecting updates.
-   **Ordering:** Improved default ordering for querysets.

---

### `Rating` Model Updates

Validation logic was added to ensure data integrity.

-   **Custom Validation Logic (`clean()` method):**
    -   Ensures members can only submit a rating *after* their associated reservation `end_date` has passed.
    -   Validates that the `rating_value` is within the allowed range (e.g., 1 to 5).
-   **Updated `save()` Method:** Enforces the validation rules before saving.
-   **Ordering:** Improved default ordering for querysets.

---

### General Meta and Constraint Changes

-   Model `Meta` options were updated to improve default ordering for `Reservation` and `Rating`.
-   Some previously strict database constraints (like `unique=True` on `Member.contact`) were removed in favor of more flexible custom validation logic within the model's `clean()` and `save()` methods.



# UniHaven API Documentation


**Base URL:** (Assuming standard Django REST Framework router registration) `/api/v1/`

---

## 1. Accommodations

Manages accommodation listings.

**Model Fields:**

*   `id` (integer, read-only): Unique identifier.
*   `room_number` (integer, nullable): Room number within a flat.
*   `flat_number` (string): Flat identifier (e.g., '1', 'C').
*   `floor_number` (integer): Floor number.
*   `building_name` (string): Name of the building.
*   `availability_start` (date): Date when the accommodation becomes available (YYYY-MM-DD).
*   `availability_end` (date): Date until which the accommodation is available (YYYY-MM-DD).
*   `number_of_beds` (integer): Number of beds in the room/flat.
*   `managed_by` (string): Entity managing the accommodation.
*   `latitude` (float, read-only, nullable): Calculated latitude.
*   `longitude` (float, read-only, nullable): Calculated longitude.
*   `distance_to_HKUcampus` (float, read-only, nullable): Calculated distance to HKU Main Campus (km).
*   `distance_to_HKUcampus_sassoon` (float, read-only, nullable): Calculated distance to HKU Sassoon Road Campus (km).
*   `distance_to_HKUcampus_kadoorie` (float, read-only, nullable): Calculated distance to HKU Kadoorie Centre (km).
*   `distance_to_CUHKcampus` (float, read-only, nullable): Calculated distance to CUHK Campus (km).
*   `distance_to_HKUSTcampus` (float, read-only, nullable): Calculated distance to HKUST Campus (km).
*   `active` (boolean): Whether the listing is active.

**Note:** Latitude, longitude, and distances are automatically calculated based on `building_name` when an accommodation is saved or updated. Requires a valid Google Maps API key configured in `models.py`.

### Endpoints

#### List Accommodations

*   **Method:** `GET`
*   **URL:** `/api/accommodations/`
*   **Description:** Retrieves a list of all accommodations. Supports searching and ordering.
*   **Query Parameters:**
    *   `search` (string): Filters results by `building_name` or `managed_by`.
    *   `ordering` (string): Field to order by (e.g., `building_name`, `-floor_number`). Default: `building_name`, `floor_number`, `flat_number`.
*   **Sample Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "room_number": 101,
            "flat_number": "A",
            "floor_number": 1,
            "building_name": "Example Tower 1",
            "availability_start": "2025-08-01",
            "availability_end": "2026-07-31",
            "number_of_beds": 1,
            "managed_by": "UniHaven Estates",
            "latitude": 22.2831,
            "longitude": 114.1366,
            "distance_to_HKUcampus": 0.1,
            "distance_to_HKUcampus_sassoon": 2.5,
            "distance_to_HKUcampus_kadoorie": 18.5,
            "distance_to_CUHKcampus": 15.1,
            "distance_to_HKUSTcampus": 16.2,
            "active": true
        },
        {
            "id": 2,
            "room_number": null,
            "flat_number": "5",
            "floor_number": 3,
            "building_name": "Student Residence B",
            "availability_start": "2025-09-01",
            "availability_end": "2026-06-30",
            "number_of_beds": 2,
            "managed_by": "Campus Housing",
            "latitude": 22.3964,
            "longitude": 114.2002,
            "distance_to_HKUcampus": 15.1,
            "distance_to_HKUcampus_sassoon": 18.0,
            "distance_to_HKUcampus_kadoorie": 9.1,
            "distance_to_CUHKcampus": 0.05,
            "distance_to_HKUSTcampus": 7.5,
            "active": true
        }
    ]
    ```

#### Create Accommodation

*   **Method:** `POST`
*   **URL:** `/api/accommodations/`
*   **Description:** Creates a new accommodation listing. Latitude/longitude/distances are calculated automatically.
*   **Sample Request Body:**
    ```json
    {
        "room_number": 205,
        "flat_number": "B",
        "floor_number": 2,
        "building_name": "Harbour View Apartments",
        "availability_start": "2025-09-15",
        "availability_end": "2026-08-31",
        "number_of_beds": 1,
        "managed_by": "Private Landlord",
        "active": true
    }
    ```
*   **Sample Response (201 Created):** (Includes calculated fields)
    ```json
    {
        "id": 3,
        "room_number": 205,
        "flat_number": "B",
        "floor_number": 2,
        "building_name": "Harbour View Apartments",
        "availability_start": "2025-09-15",
        "availability_end": "2026-08-31",
        "number_of_beds": 1,
        "managed_by": "Private Landlord",
        "latitude": 22.2850, // Example calculated value
        "longitude": 114.1580, // Example calculated value
        "distance_to_HKUcampus": 2.1, // Example calculated value
        "distance_to_HKUcampus_sassoon": 4.0, // Example calculated value
        "distance_to_HKUcampus_kadoorie": 20.0, // Example calculated value
        "distance_to_CUHKcampus": 13.5, // Example calculated value
        "distance_to_HKUSTcampus": 14.8, // Example calculated value
        "active": true
    }
    ```

#### Retrieve Accommodation

*   **Method:** `GET`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Retrieves details of a specific accommodation.
*   **Sample Response (200 OK):** (Similar structure to one item in the list response)

#### Update Accommodation

*   **Method:** `PUT`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Updates all fields of an existing accommodation. Requires all non-read-only fields. Recalculates distances if `building_name` changes.
*   **Sample Request Body:** (Provide all fields)
    ```json
    {
        "room_number": 101,
        "flat_number": "A",
        "floor_number": 1,
        "building_name": "Example Tower 1 - Updated", // Name changed
        "availability_start": "2025-08-01",
        "availability_end": "2026-07-31",
        "number_of_beds": 1,
        "managed_by": "UniHaven Estates",
        "active": true
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object with potentially new calculated distances)

#### Partial Update Accommodation

*   **Method:** `PATCH`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Updates specific fields of an existing accommodation. Recalculates distances if `building_name` changes.
*   **Sample Request Body:**
    ```json
    {
        "availability_end": "2026-08-15",
        "active": false
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Delete Accommodation

*   **Method:** `DELETE`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Deletes an accommodation listing.
*   **Sample Response (204 No Content):** (Empty body)

#### Ranked by Distance (Custom Action)

*   **Method:** `GET`
*   **URL:** `/api/accommodations/ranked_by_distance/`
*   **Description:** Retrieves accommodations ranked by distance to the main HKU campus.
*   **Query Parameters:**
    *   `reverse` (boolean, optional): If `true`, ranks by farthest first. Default is `false` (closest first).
*   **Sample Response (200 OK):** (List of accommodations ordered by `distance_to_HKUcampus`)

---

## 2. Members

Manages member information.

**Model Fields:**

*   `id` (integer, read-only): Unique identifier.
*   `name` (string): Member's full name.
*   `contact` (string): Contact information (e.g., phone number).
*   `institute` (string): Member's affiliated institute (e.g., HKU, CUHK).
*   `email` (string): Member's email address.
*   `active` (boolean): Whether the member account is active.

### Endpoints

#### List Members

*   **Method:** `GET`
*   **URL:** `/api/members/`
*   **Description:** Retrieves a list of all members. Supports searching and ordering.
*   **Query Parameters:**
    *   `search` (string): Filters results by `name`, `contact`, or `institute`.
    *   `ordering` (string): Field to order by (e.g., `name`, `-institute`). Default: `name`.
*   **Sample Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "name": "Alice Wonderland",
            "contact": "+852-98765432",
            "institute": "HKU",
            "email": "alice@example.hku.hk",
            "active": true
        },
        {
            "id": 2,
            "name": "Bob The Builder",
            "contact": "61234567",
            "institute": "CUHK",
            "email": "bob@example.cuhk.edu.hk",
            "active": true
        }
    ]
    ```

#### Create Member

*   **Method:** `POST`
*   **URL:** `/api/members/`
*   **Description:** Creates a new member.
*   **Sample Request Body:**
    ```json
    {
        "name": "Charlie Chaplin",
        "contact": "5555-1234",
        "institute": "HKUST",
        "email": "charlie@example.ust.hk",
        "active": true
    }
    ```
*   **Sample Response (201 Created):**
    ```json
    {
        "id": 3,
        "name": "Charlie Chaplin",
        "contact": "5555-1234",
        "institute": "HKUST",
        "email": "charlie@example.ust.hk",
        "active": true
    }
    ```

#### Retrieve Member

*   **Method:** `GET`
*   **URL:** `/api/members/{id}/`
*   **Description:** Retrieves details of a specific member.
*   **Sample Response (200 OK):** (Similar structure to one item in the list response)

#### Update Member

*   **Method:** `PUT`
*   **URL:** `/api/members/{id}/`
*   **Description:** Updates all fields of an existing member. Requires all fields.
*   **Sample Request Body:** (Provide all fields)
    ```json
    {
        "name": "Alice W. Wonderland",
        "contact": "+852-98765432",
        "institute": "HKU",
        "email": "alice.w@example.hku.hk",
        "active": true
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Partial Update Member

*   **Method:** `PATCH`
*   **URL:** `/api/members/{id}/`
*   **Description:** Updates specific fields of an existing member.
*   **Sample Request Body:**
    ```json
    {
        "contact": "9876-0000",
        "active": false
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Delete Member

*   **Method:** `DELETE`
*   **URL:** `/api/members/{id}/`
*   **Description:** Deletes a member.
*   **Sample Response (204 No Content):** (Empty body)

---

## 3. Reservations

Manages reservations of accommodations by members.

**Model Fields:**

*   `id` (integer, read-only): Unique identifier.
*   `accommodation` (integer): ID of the reserved accommodation.
*   `member` (integer): ID of the reserving member.
*   `start_date` (date): Reservation start date (YYYY-MM-DD).
*   `end_date` (date): Reservation end date (YYYY-MM-DD).
*   `status` (string): Reservation status. Choices: `Signed`, `Not Signed`.
*   `active` (boolean): Whether the reservation record itself is active.

**Validation Rules:**

*   `start_date` must not be after `end_date`.
*   Cannot set `active` to `false` if `status` is `Signed`.
*   Prevents creation/update if the reservation period overlaps with another *active* reservation for the *same* accommodation.
*   An email notification is sent to the member if the `active` status changes upon saving. Requires email settings configured in Django (`settings.py`).

### Endpoints

#### List Reservations

*   **Method:** `GET`
*   **URL:** `/api/reservations/`
*   **Description:** Retrieves a list of all reservations. Supports searching and ordering.
*   **Query Parameters:**
    *   `search` (string): Filters results by `accommodation__building_name`, `member__name`, or `status`.
    *   `ordering` (string): Field to order by (e.g., `start_date`, `-end_date`). Default: `start_date`.
*   **Sample Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "accommodation": 1, // ID of Accommodation
            "member": 1, // ID of Member
            "start_date": "2025-08-15",
            "end_date": "2026-01-15",
            "status": "Signed",
            "active": true
        },
        {
            "id": 2,
            "accommodation": 2,
            "member": 2,
            "start_date": "2025-09-01",
            "end_date": "2026-06-30",
            "status": "Not Signed",
            "active": true
        }
    ]
    ```

#### Create Reservation

*   **Method:** `POST`
*   **URL:** `/api/reservations/`
*   **Description:** Creates a new reservation. Validates against overlapping dates and status rules.
*   **Sample Request Body:**
    ```json
    {
        "accommodation": 1,
        "member": 2,
        "start_date": "2026-02-01",
        "end_date": "2026-07-31",
        "status": "Not Signed",
        "active": true
    }
    ```
*   **Sample Response (201 Created):**
    ```json
    {
        "id": 3,
        "accommodation": 1,
        "member": 2,
        "start_date": "2026-02-01",
        "end_date": "2026-07-31",
        "status": "Not Signed",
        "active": true
    }
    ```
*   **Sample Error Response (400 Bad Request - Overlap):**
    ```json
    {
        "non_field_errors": [
            "This accommodation is already reserved during the period 2026-02-01 to 2026-07-31."
        ]
    }
    ```
*   **Sample Error Response (400 Bad Request - Inactive Signed):**
    ```json
    {
        "non_field_errors": [
            "A reservation with a signed contract cannot be set to inactive."
        ]
    }
    ```

#### Retrieve Reservation

*   **Method:** `GET`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Retrieves details of a specific reservation.
*   **Sample Response (200 OK):** (Similar structure to one item in the list response)

#### Update Reservation

*   **Method:** `PUT`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Updates all fields of an existing reservation. Requires all fields. Validates rules. Sends email if `active` changes.
*   **Sample Request Body:** (Provide all fields)
    ```json
    {
        "accommodation": 2,
        "member": 2,
        "start_date": "2025-09-01",
        "end_date": "2026-06-30",
        "status": "Signed", // Status changed
        "active": true
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Partial Update Reservation

*   **Method:** `PATCH`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Updates specific fields of an existing reservation. Validates rules. Sends email if `active` changes.
*   **Sample Request Body:**
    ```json
    {
        "status": "Signed"
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Delete Reservation

*   **Method:** `DELETE`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Deletes a reservation.
*   **Sample Response (204 No Content):** (Empty body)

#### Get Unsigned/Signed Reservations (Custom Action)

*   **Method:** `GET`
*   **URL:** `/api/reservations/get_Unsigned_reservations/`
*   **Description:** Retrieves reservations based on their signed status.
*   **Query Parameters:**
    *   `unsigned` (boolean, optional): If `true`, returns 'Signed' reservations. If `false` or omitted, returns 'Not Signed' reservations.
*   **Sample Response (200 OK - ?unsigned=false):** (List of reservations with status 'Not Signed')
*   **Sample Response (200 OK - ?unsigned=true):** (List of reservations with status 'Signed')

---

## 4. Ratings

Manages member ratings for accommodations.

**Model Fields:**

*   `id` (integer, read-only): Unique identifier.
*   `accommodation` (integer): ID of the rated accommodation.
*   `member` (integer): ID of the rating member.
*   `rating` (integer): Rating value (1-5).
*   `comment` (string, nullable): Optional text comment.
*   `active` (boolean): Whether the rating is active.

**Validation Rules:**

*   `rating` must be between 1 and 5 (inclusive).
*   A member can only rate an accommodation *after* their reservation period for that specific accommodation has ended.
*   A member can only rate a specific accommodation once (`unique_together` constraint).

### Endpoints

#### List Ratings

*   **Method:** `GET`
*   **URL:** `/api/ratings/`
*   **Description:** Retrieves a list of all ratings. Supports searching and ordering.
*   **Query Parameters:**
    *   `search` (string): Filters results by `accommodation__building_name`, `member__name`, or `rating`.
    *   `ordering` (string): Field to order by (e.g., `rating`, `-member`). Default: `-rating`.
*   **Sample Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "accommodation": 1,
            "member": 1,
            "rating": 5,
            "comment": "Great location, very convenient!",
            "active": true
        },
        {
            "id": 2,
            "accommodation": 2,
            "member": 2,
            "rating": 4,
            "comment": null,
            "active": true
        }
    ]
    ```

#### Create Rating

*   **Method:** `POST`
*   **URL:** `/api/ratings/`
*   **Description:** Creates a new rating. Validates rating value and checks if the member had a completed reservation for the accommodation.
*   **Sample Request Body:**
    ```json
    {
        "accommodation": 1,
        "member": 1, // Assuming member 1 had a past reservation for accommodation 1
        "rating": 4,
        "comment": "Clean and tidy.",
        "active": true
    }
    ```
*   **Sample Response (201 Created):**
    ```json
    {
        "id": 3,
        "accommodation": 1,
        "member": 1,
        "rating": 4,
        "comment": "Clean and tidy.",
        "active": true
    }
    ```
*   **Sample Error Response (400 Bad Request - No Completed Reservation):**
    ```json
    {
        "non_field_errors": [
            "You can only rate an accommodation after your reservation period has ended."
        ]
    }
    ```
*   **Sample Error Response (400 Bad Request - Invalid Rating):**
    ```json
    {
        "rating": [
            "Rating must be between 1 and 5."
        ]
    }
    ```
*   **Sample Error Response (400 Bad Request - Already Rated):**
    ```json
    {
        "non_field_errors": [
            "The fields accommodation, member must make a unique set."
        ]
    }
    ```

#### Retrieve Rating

*   **Method:** `GET`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Retrieves details of a specific rating.
*   **Sample Response (200 OK):** (Similar structure to one item in the list response)

#### Update Rating

*   **Method:** `PUT`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Updates all fields of an existing rating. Requires all fields. Validates rules.
*   **Sample Request Body:** (Provide all fields)
    ```json
    {
        "accommodation": 1,
        "member": 1,
        "rating": 5, // Rating updated
        "comment": "Updated: Still great!",
        "active": true
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Partial Update Rating

*   **Method:** `PATCH`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Updates specific fields of an existing rating. Validates rules.
*   **Sample Request Body:**
    ```json
    {
        "comment": "Just a small update to the comment.",
        "active": false
    }
    ```
*   **Sample Response (200 OK):** (Returns the updated object)

#### Delete Rating

*   **Method:** `DELETE`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Deletes a rating.
*   **Sample Response (204 No Content):** (Empty body)

#### Ranked by Rating (Custom Action)

*   **Method:** `GET`
*   **URL:** `/api/ratings/ranked_by_rating/`
*   **Description:** Retrieves ratings ranked by the rating value.
*   **Query Parameters:**
    *   `reverse` (boolean, optional): If `true`, ranks lowest rating first (1-5). Default is `false` (highest first, 5-1).
*   **Sample Response (200 OK):** (List of ratings ordered by `rating`)

---



## Test Cases

The `tests.py` for the Django application's serializers, use Django's `TestCase` framework to ensure the serializers function correctly.

## `AccommodationSerializerTest`

This class tests the `AccommodationSerializer`.

*   **`setUp(self)`:**
    *   Creates a dictionary `self.accommodation_attributes` with sample data for an `Accommodation`.
    *   Creates an `Accommodation` instance in the test database using these attributes.
    *   Initializes `self.serializer` with the created `Accommodation` instance to test serialization (object to data).

*   **`test_contains_expected_fields(self)`:**
    *   Serializes the `Accommodation` instance using `self.serializer.data`.
    *   Asserts that the keys (field names) in the serialized data are exactly `{'id', 'room_number', 'flat_number', 'floor_number', 'building_name', 'availability_start', 'availability_end', 'managed_by'}`.

*   **`test_field_content(self)`:**
    *   Serializes the `Accommodation` instance.
    *   Asserts that the values for each field in the serialized data match the corresponding values in `self.accommodation_attributes` (converting dates to strings for comparison).

*   **`test_accommodation_serializer_valid_data(self)`:**
    *   Initializes an `AccommodationSerializer` with the `self.accommodation_attributes` dictionary to test deserialization/validation (data to object).
    *   Asserts that the serializer considers this data valid using `serializer.is_valid()`.

## `MemberSerializerTest`

This class tests the `MemberSerializer`.

*   **`setUp(self)`:**
    *   Creates a dictionary `self.member_attributes` with sample data for a `Member`.
    *   Creates a `Member` instance in the test database.
    *   Initializes `self.serializer` with the created `Member` instance.

*   **`test_contains_expected_fields(self)`:**
    *   Serializes the `Member` instance.
    *   Asserts that the keys in the serialized data are exactly `{'id', 'name', 'contact', 'institute'}`.

*   **`test_field_content(self)`:**
    *   Serializes the `Member` instance.
    *   Asserts that the values for each field in the serialized data match the corresponding values in `self.member_attributes`.

*   **`test_member_serializer_valid_data(self)`:**
    *   Creates a *new* dictionary `valid_data_for_creation` with different valid data for a `Member`.
    *   Initializes a `MemberSerializer` with this new data.
    *   Asserts that the serializer considers this data valid using `serializer.is_valid(raise_exception=True)`. `raise_exception=True` provides detailed error messages if validation fails.

## `ReservationSerializerTest`

This class tests the `ReservationSerializer`.

*   **`setUp(self)`:**
    *   Creates prerequisite `Accommodation` and `Member` instances.
    *   Creates a dictionary `self.reservation_attributes` with sample data for a `Reservation`, using the IDs of the created accommodation and member.
    *   Creates a `Reservation` instance in the test database using the related objects.
    *   Initializes `self.serializer` with the created `Reservation` instance.

*   **`test_contains_expected_fields(self)`:**
    *   Serializes the `Reservation` instance.
    *   Asserts that the keys in the serialized data are exactly `{'id', 'accommodation', 'start_date', 'end_date', 'member', 'status'}`.

*   **`test_field_content(self)`:**
    *   Serializes the `Reservation` instance.
    *   Asserts that the values for each field in the serialized data match the corresponding values in `self.reservation_attributes` (using IDs for foreign keys and string representations for dates).

*   **`test_reservation_serializer_valid_data(self)`:**
    *   Creates a *new* dictionary `valid_data_for_creation` with different valid data (specifically different dates) for a `Reservation`.
    *   Initializes a `ReservationSerializer` with this new data.
    *   Asserts that the serializer considers this data valid using `serializer.is_valid(raise_exception=True)`.

## `RatingSerializerTest`

This class tests the `RatingSerializer`.

*   **`setUp(self)`:**
    *   Creates prerequisite `Accommodation` and `Member` instances.
    *   Creates a dictionary `self.rating_attributes` with sample data for a `Rating`, using the IDs of the created accommodation and member.
    *   Creates a `Rating` instance in the test database.
    *   Initializes `self.serializer` with the created `Rating` instance.

*   **`test_contains_expected_fields(self)`:**
    *   Serializes the `Rating` instance.
    *   Asserts that the keys in the serialized data are exactly `{'id', 'accommodation', 'member', 'rating', 'comment'}`.

*   **`test_field_content(self)`:**
    *   Serializes the `Rating` instance.
    *   Asserts that the values for each field in the serialized data match the corresponding values in `self.rating_attributes` (using IDs for foreign keys).

*   **Note:** This test class does not currently include a `test_rating_serializer_valid_data` method to explicitly test the validation of new rating data during creation/deserialization.
