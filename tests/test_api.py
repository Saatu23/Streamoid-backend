from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_upload_and_list():
    csv_content = """sku,name,brand,color,size,mrp,price,quantity\nTSHIRT-RED-001,Classic Cotton T-Shirt,Stream Threads,Red,M,799,499,20\n"""
    response = client.post("/upload", files={"file": ("products.csv", csv_content)})
    assert response.status_code == 200
    data = response.json()
    assert data["stored"] == 1
    assert data["failed"] == []

    response = client.get("/products?page=1&limit=10")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert products[0]["sku"] == "TSHIRT-RED-001"

def test_search():
    response = client.get("/products/search?brand=Stream Threads&color=Red&minPrice=400&maxPrice=800")
    assert response.status_code == 200
    products = response.json()
    assert any(p["sku"] == "TSHIRT-RED-001" for p in products)
