import sqlite3
import uuid
from db import get_connection

def add_landlord(name: str, email: str, phone: str) -> str:
    """add landlord, return landlord UUID"""
    conn = get_connection()
    cursor = conn.cursor()
    landlord_id = str(uuid.uuid4())

    try:
        cursor.execute("""
        INSERT INTO landlords (id, name, email, phone)
        VALUES (?, ?, ?, ?)
        """, (landlord_id, name, email, phone))
        conn.commit()
        print(f"Landlord added: {name} ({landlord_id})")
        return landlord_id
    except sqlite3.IntegrityError as e:
        print("add ：", e)
        return None
    finally:
        conn.close()

def get_all_landlords() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone FROM landlords")
    rows = cursor.fetchall()
    conn.close()

    landlords = []
    for row in rows:
        landlords.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3]
        })
    return landlords