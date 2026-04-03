"""Migration: Add priority and due_date columns to task table."""
import os
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Check existing columns
    result = conn.execute(sqlalchemy.text(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'task'"
    ))
    columns = [row[0] for row in result.fetchall()]
    print('Existing columns:', columns)

    if 'priority' not in columns:
        conn.execute(sqlalchemy.text("ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium'"))
        print('Added priority column')
    else:
        print('priority column already exists')

    if 'due_date' not in columns:
        conn.execute(sqlalchemy.text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP DEFAULT NULL"))
        print('Added due_date column')
    else:
        print('due_date column already exists')

    conn.commit()

print('Migration complete!')
