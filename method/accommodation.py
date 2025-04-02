import sqlite3
import json
import uuid
from db import get_connection

def add_accommodation(data: dict) -> str:
    """Add accommodation, return accommodation UUID"""
    conn = get_connection()
    cursor = conn.cursor()
    accommodation_id = str(uuid.uuid4())

    cursor.execute("""
    INSERT INTO accommodations (
        id, type, period_of_availability, number_of_rooms_available,
        shared_bathroom, price, location, latitude, longitude,
        amenities, photos, landlord_id, availability_calendar,
        description, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        accommodation_id,
        data.get("type"),
        data.get("period_of_availability"),
        data.get("number_of_rooms_available"),
        int(data.get("shared_bathroom", 0)),
        data.get("price"),
        data.get("location"),
        data.get("latitude"),
        data.get("longitude"),
        json.dumps(data.get("amenities", [])),
        json.dumps(data.get("photos", [])),
        data.get("landlord_id"),
        json.dumps(data.get("availability_calendar", [])),
        data.get("description"),
        data.get("created_at"),
        data.get("updated_at")
    ))
    
    conn.commit()
    conn.close()
    return accommodation_id

def delete_accommodation(accommodation_id: str) -> bool:
    """Delete accommodation by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accommodations WHERE id = ?", (accommodation_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return False
    return True

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


def get_accommodation_details(accommodation_id: str) -> dict:
    """Get accommodation details by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accommodations WHERE id = ?", (accommodation_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    columns = [col[0] for col in cursor.description]
    data = dict(zip(columns, row))

    data["amenities"] = json.loads(data["amenities"]) if data["amenities"] else []
    data["photos"] = json.loads(data["photos"]) if data["photos"] else []
    data["availability_calendar"] = json.loads(data["availability_calendar"]) if data["availability_calendar"] else []

    return data


def get_listing_preview(listing: dict) -> dict:
    """Get a preview of the accommodation listing"""
    return {
        "id": listing["id"],
        "photo": listing["photos"][0] if listing["photos"] else None,
        "type": listing["type"],
        "price": listing["price"],
        "location": listing["location"]
    }
