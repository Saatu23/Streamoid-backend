# Streamoid Product Catalog Backend

A small, production-oriented backend that lets sellers validate and preview product CSVs before listing to marketplaces. It provides a CSV upload endpoint that validates rows, stores valid products in SQLite, and exposes REST APIs to list and search products.

Contents
- `main.py` — FastAPI application and endpoints
- `models.py` — SQLAlchemy Product model
- `database.py` — SQLite engine and session factory
- `crud.py` — create/get/search helper functions
- `utils.py` — CSV parsing and validation rules
- `scripts/seed_db.py` — helper to seed DB from `example_products.csv`
- `example_products.csv` — sample data
- `Dockerfile`, `docker-compose.yml` — containerization assets
- `requirements.txt`, `tests/` — dependencies and unit tests

Key deliverables
- REST API with endpoints:
  - `POST /upload` — upload CSV, validate rows, store valid rows
  - `GET /products` — list products (pagination: `?page=1&limit=10`)
  - `GET /products/search` — search by `brand`, `color`, `minPrice`, `maxPrice`
- Example CSV and seed script
- Docker image export (`.tar`) for delivery

Quick start (local, development)
1. Create and activate a virtual environment (PowerShell):
```powershell
cd 'C:\Users\satya\Desktop\Streamoid'
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```
2. Install dependencies:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```
3. (Optional) seed the database with sample data:
```powershell
python -m scripts.seed_db
```
4. Run the API server (development):
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Open the Swagger UI at: http://localhost:8000/docs

API reference (examples shown as you would see in the UI)

1) POST /upload — Upload a CSV file

Request (form-data)
- file: choose CSV file (headers expected: `sku,name,brand,color,size,mrp,price,quantity`)

Successful response (example shown in UI):
```json
{
  "stored": 12,
  "failed": [
    { "sku": "TSHIRT-RED-001", "errors": ["duplicate_or_constraint_error"] },
    { "sku": "BAD-ROW-123", "errors": ["Missing mrp","Invalid number format"] }
  ]
}
```

Notes on validation
- `price` must be less than or equal to `mrp`
- `quantity` must be a non-negative integer
- Required fields: `sku`, `name`, `brand`, `mrp`, `price`

2) GET /products — List products (paginated)

Request URL example:
```
GET /products?page=1&limit=10
```

Response (example):
```json
[
  {
    "sku": "TSHIRT-RED-001",
    "name": "Classic Cotton T-Shirt",
    "brand": "Stream Threads",
    "color": "Red",
    "size": "M",
    "mrp": 799,
    "price": 499,
    "quantity": 20
  },
  {
    "sku": "JEANS-BLU-032",
    "name": "Slim Fit Jeans",
    "brand": "DenimWorks",
    "color": "Blue",
    "size": "32",
    "mrp": 1999,
    "price": 1599,
    "quantity": 15
  }
]
```

3) GET /products/search — Search and filter

Request URL examples:
```
GET /products/search?brand=StreamThreads
GET /products/search?color=Red
GET /products/search?minPrice=500&maxPrice=2000
```

Response (example):
```json
[
  {
    "sku": "DRESS-PNK-S",
    "name": "Floral Summer Dress",
    "brand": "BloomWear",
    "color": "Pink",
    "size": "S",
    "mrp": 2499,
    "price": 2199,
    "quantity": 10
  }
]
```

Testing
```powershell
pytest -q
```

Docker - save (.tar), build, load, run

This project supports containerized delivery. Below are the exact commands to build the image locally or download from drive, and load/run it on the recipient system.

1) Download the same Docker image from below Drive link
```powershell
https://drive.google.com/file/d/1wnpET_nL4kFVkMHuLg2Tq-mGnDGCLh9I/view?usp=sharing
```

2) Build the Docker image locally
```powershell
docker build -t streamoid-backend .
```

3) Recipient loads the image and runs it
```powershell
# load the image from tar
docker load -i streamoid-backend.tar

# run the container
docker run --rm -p 8000:8000 streamoid-backend

# access the Swagger UI at http://localhost:8000/docs
```
