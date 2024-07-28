from app import db, app
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(user)")).fetchall()
        columns = [row[1] for row in result]

        if 'status' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN status TEXT DEFAULT "Not started"'))

        if 'is_admin' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0'))

print("Database migration completed.")
