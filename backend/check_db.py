import os
from src.database import engine
from sqlalchemy import text

# Print the database URL that's being used
print("Current DATABASE_URL from environment:", os.getenv("DATABASE_URL", "sqlite:///./todoapp.db"))

# Print the engine URL
print("Engine URL:", engine.url)

# Test the connection more explicitly
try:
    with engine.connect() as conn:
        print("Connection successful!")

        # Check if the task table exists using SQLAlchemy text
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename = 'task';"))
        rows = result.fetchall()
        table_exists = len(rows) > 0
        print(f"Task table exists: {table_exists}")

        # Check if the user table exists
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename = 'user';"))
        rows = result.fetchall()
        user_table_exists = len(rows) > 0
        print(f"User table exists: {user_table_exists}")

        if not table_exists or not user_table_exists:
            print("Some tables do not exist in the database!")
            # Let's see what tables do exist
            result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
            existing_tables = result.fetchall()
            print(f"Existing tables in public schema: {[table[0] for table in existing_tables]}")
        else:
            print("All required tables exist in the database!")

        # Try to create the tables explicitly again (including User model)
        print("\nAttempting to create tables explicitly...")
        from src.models.task_model import Task
        from src.models.user_model import User
        from src.models.session_model import Session
        from sqlmodel import SQLModel
        try:
            SQLModel.metadata.create_all(engine)
            print("Tables creation attempt completed successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

except Exception as e:
    print(f"Connection failed: {e}")