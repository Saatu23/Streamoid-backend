from fastapi import FastAPI, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine
import crud, models, schemas, utils
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    products, failed = utils.parse_and_validate_csv(content.decode())
    stored = 0
    # insert each product in its own session so one failure doesn't break the whole upload
    for product in products:
        db: Session = SessionLocal()
        try:
            crud.create_product(db, product)
            stored += 1
        except IntegrityError as ie:
            # likely a duplicate SKU or constraint failure
            try:
                db.rollback()
            except Exception:
                pass
            failed.append({"sku": getattr(product, "sku", None), "errors": ["duplicate_or_constraint_error"]})
        except Exception as e:
            try:
                db.rollback()
            except Exception:
                pass
            failed.append({"sku": getattr(product, "sku", None), "errors": [str(e)]})
        finally:
            db.close()

    return {"stored": stored, "failed": failed}

@app.get("/products", response_model=List[schemas.Product])
def list_products(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    db: Session = SessionLocal()
    products = crud.get_products(db, page, limit)
    db.close()
    return products

@app.get("/products/search", response_model=List[schemas.Product])
def search_products(
    brand: Optional[str] = None,
    color: Optional[str] = None,
    minPrice: Optional[int] = None,
    maxPrice: Optional[int] = None,
):
    db: Session = SessionLocal()
    products = crud.search_products(db, brand, color, minPrice, maxPrice)
    db.close()
    return products
