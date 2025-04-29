---
title:  API Design for UniHaven Accommodation Management System
author: COMP3297 Group E
geometry: margin=1cm
---

# UniHaven API Documentation

This document provides details about the API endpoints for managing Accommodations, Members, Reservations, and Ratings. The API is built using Django REST Framework and utilizes a `DefaultRouter` for URL generation.

**Base URL:** `/api/` (Assuming the `basic` app URLs are included under `/api/` in your project's main `urls.py`)

---

## 1. Accommodations

Endpoints for managing accommodation listings.

**Model Fields:**
*   `id` (Integer, Read-only)
*   `room_number` (Integer, Nullable)
*   `flat_number` (String)
*   `floor_number` (Integer)
*   `building_name` (String)
*   `availability_start` (Date, YYYY-MM-DD)
*   `availability_end` (Date, YYYY-MM-DD)
*   `managed_by` (String)

### List Accommodations

*   **Method:** `GET`
*   **URL:** `/api/accommodations/`
*   **Description:** Retrieves a list of all available accommodations.
*   **Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "room_number": 101,
            "flat_number": "A",
            "floor_number": 1,
            "building_name": "Main Hall",
            "availability_start": "2025-09-01",
            "availability_end": "2026-06-30",
            "managed_by": "University Housing"
        },
        {
            "id": 2,
            "room_number": null,
            "flat_number": "B2",
            "floor_number": 2,
            "building_name": "West Wing",
            "availability_start": "2025-08-15",
            "availability_end": "2026-07-31",
            "managed_by": "Private Owner"
        }
        // ... more accommodations
    ]
    ```

### Create Accommodation

*   **Method:** `POST`
*   **URL:** `/api/accommodations/`
*   **Description:** Creates a new accommodation record.
*   **Request Body:**
    ```json
    {
        "room_number": 205,
        "flat_number": "C",
        "floor_number": 2,
        "building_name": "North Tower",
        "availability_start": "2025-09-01",
        "availability_end": "2026-08-31",
        "managed_by": "Campus Services"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
        "id": 3,
        "room_number": 205,
        "flat_number": "C",
        "floor_number": 2,
        "building_name": "North Tower",
        "availability_start": "2025-09-01",
        "availability_end": "2026-08-31",
        "managed_by": "Campus Services"
    }
    ```

### Retrieve Accommodation

*   **Method:** `GET`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Retrieves details of a specific accommodation by its ID.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the accommodation to retrieve.
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "room_number": 101,
        "flat_number": "A",
        "floor_number": 1,
        "building_name": "Main Hall",
        "availability_start": "2025-09-01",
        "availability_end": "2026-06-30",
        "managed_by": "University Housing"
    }
    ```

### Update Accommodation

*   **Method:** `PUT`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Updates all fields of a specific accommodation. All fields are required.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the accommodation to update.
*   **Request Body:**
    ```json
    {
        "room_number": 101,
        "flat_number": "A-Updated",
        "floor_number": 1,
        "building_name": "Main Hall (Renovated)",
        "availability_start": "2025-09-01",
        "availability_end": "2026-07-15",
        "managed_by": "University Housing Dept."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "room_number": 101,
        "flat_number": "A-Updated",
        "floor_number": 1,
        "building_name": "Main Hall (Renovated)",
        "availability_start": "2025-09-01",
        "availability_end": "2026-07-15",
        "managed_by": "University Housing Dept."
    }
    ```

### Partial Update Accommodation

*   **Method:** `PATCH`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Partially updates fields of a specific accommodation. Only include fields to be changed.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the accommodation to update.
*   **Request Body:**
    ```json
    {
        "availability_end": "2026-07-30",
        "managed_by": "Updated Manager"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "room_number": 101,
        "flat_number": "A-Updated", // Assuming previous PUT/PATCH
        "floor_number": 1,
        "building_name": "Main Hall (Renovated)", // Assuming previous PUT/PATCH
        "availability_start": "2025-09-01",
        "availability_end": "2026-07-30",
        "managed_by": "Updated Manager"
    }
    ```

### Delete Accommodation

*   **Method:** `DELETE`
*   **URL:** `/api/accommodations/{id}/`
*   **Description:** Deletes a specific accommodation.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the accommodation to delete.
*   **Response (204 No Content):** (Empty response body)

---

## 2. Members

Endpoints for managing member information.

**Model Fields:**
*   `id` (Integer, Read-only)
*   `name` (String)
*   `contact` (String, Unique)
*   `institute` (String)

### List Members

*   **Method:** `GET`
*   **URL:** `/api/members/`
*   **Description:** Retrieves a list of all members.
*   **Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "name": "Alice Wonderland",
            "contact": "12345678",
            "institute": "HKU"
        },
        {
            "id": 2,
            "name": "Bob The Builder",
            "contact": "87654321",
            "institute": "CUHK"
        }
        // ... more members
    ]
    ```

### Create Member

*   **Method:** `POST`
*   **URL:** `/api/members/`
*   **Description:** Creates a new member.
*   **Request Body:**
    ```json
    {
        "name": "Charlie Chaplin",
        "contact": "11223344",
        "institute": "PolyU"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
        "id": 3,
        "name": "Charlie Chaplin",
        "contact": "11223344",
        "institute": "PolyU"
    }
    ```

### Retrieve Member

*   **Method:** `GET`
*   **URL:** `/api/members/{id}/`
*   **Description:** Retrieves details of a specific member.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the member.
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "name": "Alice Wonderland",
        "contact": "12345678",
        "institute": "HKU"
    }
    ```

### Update Member

*   **Method:** `PUT`
*   **URL:** `/api/members/{id}/`
*   **Description:** Updates all fields of a specific member.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the member.
*   **Request Body:**
    ```json
    {
        "name": "Alice W. Updated",
        "contact": "99998888",
        "institute": "HKUST"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "name": "Alice W. Updated",
        "contact": "99998888",
        "institute": "HKUST"
    }
    ```

### Partial Update Member

*   **Method:** `PATCH`
*   **URL:** `/api/members/{id}/`
*   **Description:** Partially updates fields of a specific member.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the member.
*   **Request Body:**
    ```json
    {
        "contact": "10101010"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "name": "Alice W. Updated", // From previous update
        "contact": "10101010",
        "institute": "HKUST" // From previous update
    }
    ```

### Delete Member

*   **Method:** `DELETE`
*   **URL:** `/api/members/{id}/`
*   **Description:** Deletes a specific member.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the member.
*   **Response (204 No Content):** (Empty response body)

---

## 3. Reservations

Endpoints for managing reservations.

**Model Fields:**
*   `id` (Integer, Read-only)
*   `accommodation` (Integer, Foreign Key to Accommodation ID)
*   `start_date` (Date, YYYY-MM-DD)
*   `end_date` (Date, YYYY-MM-DD)
*   `member` (Integer, Foreign Key to Member ID)
*   `status` (String, Choices: 'Signed', 'Not Signed')

### List Reservations

*   **Method:** `GET`
*   **URL:** `/api/reservations/`
*   **Description:** Retrieves a list of all reservations.
*   **Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "accommodation": 1,
            "start_date": "2025-09-01",
            "end_date": "2026-06-30",
            "member": 1,
            "status": "Signed"
        },
        {
            "id": 2,
            "accommodation": 2,
            "start_date": "2025-08-15",
            "end_date": "2026-07-31",
            "member": 2,
            "status": "Not Signed"
        }
        // ... more reservations
    ]
    ```

### Create Reservation

*   **Method:** `POST`
*   **URL:** `/api/reservations/`
*   **Description:** Creates a new reservation.
*   **Request Body:**
    ```json
    {
        "accommodation": 1,
        "start_date": "2026-07-01",
        "end_date": "2027-06-30",
        "member": 2,
        "status": "Not Signed"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
        "id": 3,
        "accommodation": 1,
        "start_date": "2026-07-01",
        "end_date": "2027-06-30",
        "member": 2,
        "status": "Not Signed"
    }
    ```

### Retrieve Reservation

*   **Method:** `GET`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Retrieves details of a specific reservation.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the reservation.
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "accommodation": 1,
        "start_date": "2025-09-01",
        "end_date": "2026-06-30",
        "member": 1,
        "status": "Signed"
    }
    ```

### Update Reservation

*   **Method:** `PUT`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Updates all fields of a specific reservation.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the reservation.
*   **Request Body:**
    ```json
    {
        "accommodation": 1,
        "start_date": "2025-09-01",
        "end_date": "2026-07-15", // Updated end date
        "member": 1,
        "status": "Signed"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "accommodation": 1,
        "start_date": "2025-09-01",
        "end_date": "2026-07-15",
        "member": 1,
        "status": "Signed"
    }
    ```

### Partial Update Reservation

*   **Method:** `PATCH`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Partially updates fields of a specific reservation.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the reservation.
*   **Request Body:**
    ```json
    {
        "status": "Signed" // Update status for reservation ID 2
    }
    ```
*   **Response (200 OK):** (Example for updating reservation ID 2)
    ```json
    {
        "id": 2,
        "accommodation": 2,
        "start_date": "2025-08-15",
        "end_date": "2026-07-31",
        "member": 2,
        "status": "Signed"
    }
    ```

### Delete Reservation

*   **Method:** `DELETE`
*   **URL:** `/api/reservations/{id}/`
*   **Description:** Deletes a specific reservation.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the reservation.
*   **Response (204 No Content):** (Empty response body)

---

## 4. Ratings

Endpoints for managing accommodation ratings.

**Model Fields:**
*   `id` (Integer, Read-only)
*   `accommodation` (Integer, Foreign Key to Accommodation ID)
*   `member` (Integer, Foreign Key to Member ID)
*   `rating` (Integer)
*   `comment` (String, Nullable)

### List Ratings

*   **Method:** `GET`
*   **URL:** `/api/ratings/`
*   **Description:** Retrieves a list of all ratings.
*   **Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "accommodation": 1,
            "member": 1,
            "rating": 5,
            "comment": "Great place!"
        },
        {
            "id": 2,
            "accommodation": 2,
            "member": 2,
            "rating": 4,
            "comment": null
        }
        // ... more ratings
    ]
    ```

### Create Rating

*   **Method:** `POST`
*   **URL:** `/api/ratings/`
*   **Description:** Creates a new rating. Note: The `unique_together` constraint in the model prevents a member from rating the same accommodation more than once.
*   **Request Body:**
    ```json
    {
        "accommodation": 1,
        "member": 2,
        "rating": 4,
        "comment": "Very convenient location."
    }
    ```
*   **Response (201 Created):**
    ```json
    {
        "id": 3,
        "accommodation": 1,
        "member": 2,
        "rating": 4,
        "comment": "Very convenient location."
    }
    ```

### Retrieve Rating

*   **Method:** `GET`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Retrieves details of a specific rating.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the rating.
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "accommodation": 1,
        "member": 1,
        "rating": 5,
        "comment": "Great place!"
    }
    ```

### Update Rating

*   **Method:** `PUT`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Updates all fields of a specific rating.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the rating.
*   **Request Body:**
    ```json
    {
        "accommodation": 1, // Usually not changed, depends on logic
        "member": 1,        // Usually not changed
        "rating": 4,
        "comment": "Good, but a bit noisy."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "accommodation": 1,
        "member": 1,
        "rating": 4,
        "comment": "Good, but a bit noisy."
    }
    ```

### Partial Update Rating

*   **Method:** `PATCH`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Partially updates fields of a specific rating.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the rating.
*   **Request Body:**
    ```json
    {
        "comment": "Actually, the noise wasn't too bad."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
        "id": 1,
        "accommodation": 1,
        "member": 1,
        "rating": 4, // From previous update
        "comment": "Actually, the noise wasn't too bad."
    }
    ```

### Delete Rating

*   **Method:** `DELETE`
*   **URL:** `/api/ratings/{id}/`
*   **Description:** Deletes a specific rating.
*   **URL Parameters:**
    *   `id` (Integer): The ID of the rating.
*   **Response (204 No Content):** (Empty response body)

---
