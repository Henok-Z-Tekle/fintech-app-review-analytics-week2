"""
insert_reviews.py
Inserts cleaned + sentiment-labeled reviews into PostgreSQL
"""

import pandas as pd
from db_connection import get_connection
from config import DATA_PATHS


def insert_reviews():
    df = pd.read_csv(DATA_PATHS["sentiment_reviews"])  # reviews_with_sentiment.csv

    conn = get_connection()
    cur = conn.cursor()

    # Get bank_id mapping
    cur.execute("SELECT bank_id, bank_code FROM banks;")
    bank_map = {code: bid for bid, code in cur.fetchall()}

    sql = """
    INSERT INTO reviews (
        review_id, bank_id, review_text, rating, review_date,
        thumbs_up, user_name, reply, app_version,
        sentiment, text_length, scraped_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (review_id) DO NOTHING;
    """

    success = 0
    fail = 0

    for _, row in df.iterrows():
        try:
            bank_id = bank_map[row["bank_code"]]

            cur.execute(sql, (
                row["review_id"],
                bank_id,
                row["review_text"],
                row["rating"],
                row["review_date"],
                row.get("thumbs_up", 0),
                row.get("user_name", "Anonymous"),
                row.get("reply", None),
                row.get("app_version", None),
                row.get("sentiment", None),
                row.get("text_length", None),
                row.get("scraped_at", None)
            ))
            success += 1
        except Exception as e:
            fail += 1
            print(f"❌ Insert failed for review_id={row['review_id']}: {e}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n==== INSERT SUMMARY ====")
    print(f"Inserted: {success}")
    print(f"Failed:   {fail}")


if __name__ == "__main__":
    insert_reviews()
