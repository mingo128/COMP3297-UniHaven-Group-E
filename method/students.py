import sqlite3
import uuid
import json
from db import get_connection

def apply_for_accommodation(student_id: str, accommodation_id: str, notes: str = "") -> str:
    conn = get_connection()
    cursor = conn.cursor()
    application_id = str(uuid.uuid4())
    cursor.execute("""
    INSERT INTO applications (
        id, accommodation_id, user_id, application_date, status, notes
    ) VALUES (?, ?, ?, datetime('now'), 'pending', ?)
    """, (application_id, accommodation_id, student_id, notes))
    conn.commit()
    conn.close()
    return application_id

def get_my_applications(student_id: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.id, a.application_date, a.status, acc.location, acc.price
    FROM applications a
    JOIN accommodations acc ON a.accommodation_id = acc.id
    WHERE a.user_id = ?
    ORDER BY a.application_date DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": row[0],
        "application_date": row[1],
        "status": row[2],
        "location": row[3],
        "price": row[4]
    } for row in rows]

def get_public_listings(page: int = 1, page_size: int = 10) -> list:
    """Get public listings with pagination"""
    offset = (page - 1) * page_size
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, type, price, location, photos FROM accommodations
    LIMIT ? OFFSET ?
    """, (page_size, offset))
    rows = cursor.fetchall()
    conn.close()

    listings = []
    for row in rows:
        listings.append({
            "id": row[0],
            "type": row[1],
            "price": row[2],
            "location": row[3],
            "photo": json.loads(row[4])[0] if row[4] else None
        })
    return listings

def cancel_application(application_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    conn.commit()
    result = cursor.rowcount > 0
    conn.close()
    return result

def add_review(student_id: str, accommodation_id: str, review_data: dict) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    review_id = str(uuid.uuid4())
    cursor.execute("""
    INSERT INTO reviews (
        id, accommodation_id, user_id, overall_rating, value_for_money,
        location_convenience, property_condition, landlord_communication,
        review_text, photos, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (
        review_id,
        accommodation_id,
        student_id,
        review_data.get("overall_rating"),
        review_data.get("value_for_money"),
        review_data.get("location_convenience"),
        review_data.get("property_condition"),
        review_data.get("landlord_communication"),
        review_data.get("review_text"),
        json.dumps(review_data.get("photos", [])),
    ))
    conn.commit()
    conn.close()
    return review_id