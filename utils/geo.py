from db import get_connection

def get_distance_to_hku(accommodation_id: str) -> int:
    """Get distance from accommodation to HKU"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT latitude, longitude FROM accommodations WHERE id = ?
    """, (accommodation_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    lat, lon = row
    hku_lat, hku_lon = 22.2833, 114.1492  # HKU coordinates
    distance = ((lat - hku_lat) ** 2 + (lon - hku_lon) ** 2) ** 0.5 * 100000  # in meters
    return int(distance)