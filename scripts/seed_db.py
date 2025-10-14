import os
from database import engine, Base, SessionLocal
import models
import utils
import crud

Base.metadata.create_all(bind=engine)

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'example_products.csv')

def seed():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    products, failed = utils.parse_and_validate_csv(content)
    stored = 0
    for p in products:
        db = SessionLocal()
        try:
            crud.create_product(db, p)
            stored += 1
        except Exception as e:
            # rollback and skip duplicates or other DB errors
            try:
                db.rollback()
            except Exception:
                pass
            print(f"Skipping product {p.sku}: {e}")
        finally:
            db.close()
    print(f"Seed complete. Stored={stored}, Failed rows={len(failed)}")

if __name__ == '__main__':
    seed()
