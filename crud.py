from sqlalchemy.orm import Session
from models import Product
from schemas import Product as ProductSchema

def create_product(db: Session, product: ProductSchema):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, page: int, limit: int):
    offset = (page - 1) * limit
    return db.query(Product).offset(offset).limit(limit).all()

def search_products(db: Session, brand=None, color=None, minPrice=None, maxPrice=None):
    query = db.query(Product)
    if brand:
        query = query.filter(Product.brand == brand)
    if color:
        query = query.filter(Product.color == color)
    if minPrice is not None:
        query = query.filter(Product.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(Product.price <= maxPrice)
    return query.all()
