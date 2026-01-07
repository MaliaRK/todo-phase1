import os
from sqlmodel import create_engine, Session
from src.models.user_model import User
from src.database import engine

def test_connection():
    print("Testing database connection...")
    try:
        # Test basic connection
        with Session(engine) as session:
            print("Connected successfully!")

            # Test a simple query
            from sqlmodel import select
            result = session.exec(select(User).limit(1))
            user = result.first()
            print(f"Query successful! Found user: {user}")

    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()