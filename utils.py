import csv
from schemas import Product
from typing import List, Tuple

REQUIRED_FIELDS = ["sku", "name", "brand", "mrp", "price"]

def parse_and_validate_csv(content: str) -> Tuple[List[Product], List[dict]]:
    reader = csv.DictReader(content.splitlines())
    valid = []
    failed = []
    for row in reader:
        errors = []
        for field in REQUIRED_FIELDS:
            if not row.get(field):
                errors.append(f"Missing {field}")
        try:
            mrp = int(row.get("mrp", 0))
            price = int(row.get("price", 0))
            quantity = int(row.get("quantity", 0))
        except Exception:
            errors.append("Invalid number format")
            failed.append({"row": row, "errors": errors})
            continue
        if price > mrp:
            errors.append("price > mrp")
        if quantity < 0:
            errors.append("quantity < 0")
        if errors:
            failed.append({"row": row, "errors": errors})
        else:
            valid.append(Product(
                sku=row["sku"],
                name=row["name"],
                brand=row["brand"],
                color=row.get("color"),
                size=row.get("size"),
                mrp=mrp,
                price=price,
                quantity=quantity
            ))
    return valid, failed
