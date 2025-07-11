from app.db.models import User
from app.db.session import engine, SessionLocal


def test_db_connection():
    try:
        # Test engine connection
        with engine.connect() as conn:
            print("✅ Database connection successful")

        # Test session
        db = SessionLocal()
        users = db.query(User).all()
        print(f"✅ Found {len(users)} users in database")
        db.close()

    except Exception as e:
        print(f"❌ Database connection failed: {e}")


if __name__ == "__main__":
    test_db_connection()
