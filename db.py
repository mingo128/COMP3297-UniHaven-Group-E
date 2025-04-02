import sqlite3

DB_NAME = "unihaven.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  
    return conn

def initialize_db():
    """Create tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,               -- UUID
        student_id TEXT UNIQUE NOT NULL,   -- HKU UID
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    );
    """)


    # Create Landlords table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS landlords (
        id TEXT PRIMARY KEY,               -- UUID
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    );
    """)

    # Create Accommodations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accommodations (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        period_of_availability TEXT,
        number_of_rooms_available INTEGER,
        shared_bathroom INTEGER CHECK(shared_bathroom IN (0, 1)),
        price REAL NOT NULL,
        location TEXT,
        latitude REAL,
        longitude REAL,
        amenities TEXT,
        photos TEXT,
        landlord_id TEXT NOT NULL,
        availability_calendar TEXT,
        description TEXT,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (landlord_id) REFERENCES landlords(id)
    );
    """)



    # Create Applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id TEXT PRIMARY KEY,                        -- UUID
        accommodation_id TEXT NOT NULL,             -- FOREIGN KEY -> accommodations.id
        user_id TEXT NOT NULL,                      -- FOREIGN KEY -> students.id
        application_date TEXT,                      -- timestamp
        status TEXT NOT NULL,                       -- e.g. 'pending', 'approved'
        rental_contract_start_date TEXT,            -- timestamp
        rental_contract_end_date TEXT,              -- timestamp
        notes TEXT,                                 
        FOREIGN KEY (accommodation_id) REFERENCES accommodations(id),
        FOREIGN KEY (user_id) REFERENCES students(id)
    );
    """)

    # Create Reviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,                            -- UUID
        accommodation_id TEXT NOT NULL,                 -- FOREIGN KEY -> accommodations.id
        user_id TEXT NOT NULL,                          -- FOREIGN KEY -> students.id
        overall_rating INTEGER CHECK(overall_rating BETWEEN 0 AND 5),
        value_for_money INTEGER CHECK(value_for_money BETWEEN 0 AND 5),
        location_convenience INTEGER CHECK(location_convenience BETWEEN 0 AND 5),
        property_condition INTEGER CHECK(property_condition BETWEEN 0 AND 5),
        landlord_communication INTEGER CHECK(landlord_communication BETWEEN 0 AND 5),
        review_text TEXT,
        photos TEXT,                                     -- URL
        created_at TEXT,                                 -- timestamp
        updated_at TEXT,                                 -- timestamp
        FOREIGN KEY (accommodation_id) REFERENCES accommodations(id),
        FOREIGN KEY (user_id) REFERENCES students(id)
    );
    """)

    conn.commit()
    conn.close()