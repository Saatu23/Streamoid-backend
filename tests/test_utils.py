import pytest
from utils import parse_and_validate_csv

def test_parse_and_validate_csv_valid():
    csv_content = """sku,name,brand,color,size,mrp,price,quantity\nTSHIRT-RED-001,Classic Cotton T-Shirt,Stream Threads,Red,M,799,499,20\n"""
    valid, failed = parse_and_validate_csv(csv_content)
    assert len(valid) == 1
    assert len(failed) == 0
    assert valid[0].sku == "TSHIRT-RED-001"

def test_parse_and_validate_csv_invalid():
    csv_content = """sku,name,brand,color,size,mrp,price,quantity\nTSHIRT-RED-001,Classic Cotton T-Shirt,Stream Threads,Red,M,799,899,20\n"""
    valid, failed = parse_and_validate_csv(csv_content)
    assert len(valid) == 0
    assert len(failed) == 1
    assert "price > mrp" in failed[0]["errors"]

def test_parse_and_validate_csv_missing_fields():
    csv_content = """sku,name,brand,color,size,mrp,price,quantity\n,,Stream Threads,Red,M,799,499,20\n"""
    valid, failed = parse_and_validate_csv(csv_content)
    assert len(valid) == 0
    assert len(failed) == 1
    assert "Missing sku" in failed[0]["errors"]
    assert "Missing name" in failed[0]["errors"]
    assert "Missing brand" not in failed[0]["errors"]
