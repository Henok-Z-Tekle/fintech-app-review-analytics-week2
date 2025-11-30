"""
insert_banks.py
Inserts bank metadata from app_info.csv into PostgreSQL
"""

import pandas as pd
from db_connection import get_connection
from config import DATA_PATHS


def insert_banks():
    df = pd.read_csv(DATA_PATHS["app_info"])
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    INSERT INTO banks (bank_code, bank_name, app_id)
    VALUES (%s, %s, %s)
    ON CONFLICT (bank_code)
    DO UPDATE SET bank_name = EXCLUDED.bank_name, app_id = EXCLUDED.app_id;
    """

    try:
        for _, row in df.iterrows():
            cur.execute(sql, (row["bank_code"], row["bank_name"], row["app_id"]))
        print("✅ Bank data inserted successfully.")
    except Exception as e:
        print("❌ Error inserting banks:", e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    insert_banks()
