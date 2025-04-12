import sqlite3
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")

def create_database():
    """Creates the database and the data table if it does not already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            date TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(row_data):
    """
    Insert a single row of data into the database.
    row_data should be a tuple in the form (id, date, content)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO data (id, date, content) VALUES (?, ?, ?)", row_data)
    conn.commit()
    conn.close()

def load_data_from_csv():
    """Reads the CSV file and inserts each row into the SQLite database."""
    create_database()  # Ensure the database and table are created
    with open(CSV_PATH, mode="r", newline='', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row_data = (row["id"], row["date"], row["content"])
            insert_data(row_data)

def read_all_data():
    """Retrieve all rows from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    # If running this module directly, load data from CSV into the DB.
    load_data_from_csv()
    print("Data loaded into the database.")
