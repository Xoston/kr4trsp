from app.database import SessionLocal
from app.models import Product

def seed():
    db = SessionLocal()
    if db.query(Product).count() == 0:
        db.add_all([
            Product(title="Widget", price=19.99, count=100, description="A useful widget"),
            Product(title="Gadget", price=29.99, count=50, description="A fancy gadget")
        ])
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()
