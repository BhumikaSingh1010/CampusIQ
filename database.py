import sqlite3

DB_NAME = "campusiq.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            category TEXT,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT,
            department TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_complaint(
    name,
    email,
    category,
    location,
    description,
    priority="Pending",
    department="Pending"
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (name, email, category, location, description, priority, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        category,
        location,
        description,
        priority,
        department
    ))

    conn.commit()
    conn.close()


def get_complaints():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM complaints
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def get_descriptions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT description FROM complaints
    """)

    data = cursor.fetchall()
    conn.close()

    return [row[0] for row in data]


def update_status(complaint_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE complaint_id = ?
    """, (status, complaint_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("CampusIQ database created successfully!")