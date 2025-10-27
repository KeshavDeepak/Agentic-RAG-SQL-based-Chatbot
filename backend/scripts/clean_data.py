import sqlite3
from pathlib import Path
import re

# Path to your SQLite database
db_path = Path("backend/data/adventureworks.sqlite")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Regex patterns to detect date/time-like columns
DATE_LIKE_PATTERNS = [
    r"date",          # e.g. ModifiedDate, BirthDate
    r"time",          # e.g. StartTime, EndTime
    r"timestamp",     # e.g. CreatedTimestamp
    r"created",       # e.g. CreatedAt, CreatedOn
    r"modified",      # e.g. LastModified, ModifiedAt
    r"updated",       # e.g. UpdatedOn
]

def is_date_like(column_name: str) -> bool:
    """Heuristically determine if a column name is date/time related."""
    return any(re.search(pat, column_name, re.IGNORECASE) for pat in DATE_LIKE_PATTERNS)


# Get list of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

print(f"🧹 Scanning {len(tables)} tables for date/time columns with empty strings...\n")

total_fixed = 0
skipped = 0

for table in tables:
    # Skip SQLite internal tables
    if table.startswith("sqlite_"):
        continue

    cursor.execute(f"PRAGMA table_info('{table}')")
    columns = [row[1] for row in cursor.fetchall()]

    date_cols = [col for col in columns if is_date_like(col)]
    if not date_cols:
        continue

    for col in date_cols:
        try:
            # Check if there are any empty strings
            cursor.execute(f"SELECT COUNT(*) FROM '{table}' WHERE {col} = ''")
            bad_count = cursor.fetchone()[0]

            if bad_count > 0:
                print(f"🛠  Fixing {bad_count} rows in {table}.{col}")
                cursor.execute(f"UPDATE '{table}' SET {col} = NULL WHERE {col} = ''")
                total_fixed += bad_count
        except Exception as e:
            print(f"⚠️  Skipped {table}.{col} (error: {e})")
            skipped += 1

# Commit all changes
conn.commit()
conn.close()

print(f"\n✅ Cleanup complete! Fixed {total_fixed} rows across all tables. Skipped {skipped} columns.")
