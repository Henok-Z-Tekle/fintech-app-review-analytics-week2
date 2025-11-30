"""
create_tables.py
Creates PostgreSQL tables for Week 2
"""

from db_connection import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # --- BANKS TABLE ---
    create_banks = """
    CREATE TABLE IF NOT EXISTS banks (
        bank_id SERIAL PRIMARY KEY,
        bank_code VARCHAR(10) UNIQUE,
        bank_name VARCHAR(150),
        app_id VARCHAR(200)
    );
    """

    # --- REVIEWS TABLE ---
    create_reviews = """
    CREATE TABLE IF NOT EXISTS reviews (
        review_id VARCHAR(200) PRIMARY KEY,
        bank_id INT REFERENCES banks(bank_id),
        review_text TEXT,
        rating INT,
        review_date TIMESTAMP,
        thumbs_up INT,
        user_name VARCHAR(200),
        reply TEXT,
        app_version VARCHAR(50),
        sentiment VARCHAR(50),
        text_length INT,
        scraped_at TIMESTAMP
    );
    """

    try:
        cur.execute(create_banks)
        cur.execute(create_reviews)
        print("✅ Tables created successfully.")
    except Exception as e:
        print("❌ Error creating tables:", e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_tables()
