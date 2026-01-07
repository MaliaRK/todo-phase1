import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# For PostgreSQL, add only valid connection parameters to handle connection issues
if DATABASE_URL.startswith("postgresql://"):
    # Add connection parameters to handle SSL and timeouts
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    else:
        # Check if sslmode is already set
        if "sslmode=" not in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"

    # Add connection timeout parameter only
    if "connect_timeout=" not in DATABASE_URL:
        DATABASE_URL += "&connect_timeout=30"

engine = create_engine(
    DATABASE_URL,
    echo=False,           # Set to True for SQL debugging
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=5,          # Number of connection pools
    max_overflow=10,      # Additional connections beyond pool_size
    pool_timeout=30,      # Timeout for getting a connection from the pool
    connect_args={
        "connect_timeout": 30,  # Connection timeout
    }
)

def add_user_id_column():
    print("Adding user_id column to task table...")

    # Connect to the database
    with engine.connect() as conn:
        # Check if user_id column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'task'
            AND column_name = 'user_id'
        """))

        columns = [row[0] for row in result.fetchall()]

        if 'user_id' not in columns:
            print("Adding user_id column...")

            # Add the user_id column as nullable first
            conn.execute(text("ALTER TABLE task ADD COLUMN user_id VARCHAR"))

            # Add the foreign key constraint
            try:
                conn.execute(text("ALTER TABLE task ADD CONSTRAINT fk_task_user_id FOREIGN KEY (user_id) REFERENCES user(id)"))
            except Exception as e:
                print(f"Foreign key constraint might already exist or error: {e}")

            conn.commit()
            print("Successfully added user_id column to task table!")
        else:
            print("user_id column already exists.")

if __name__ == "__main__":
    add_user_id_column()