from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User


def main():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@progym.com").first()
    if not admin:
        db.add(
            User(
                name="Platform Admin",
                email="admin@progym.com",
                password_hash=get_password_hash("Admin@12345"),
                role="admin",
                is_active=True,
            )
        )
        db.commit()
        print("Admin user seeded: admin@progym.com / Admin@12345")
    else:
        print("Admin already exists")


if __name__ == "__main__":
    main()
