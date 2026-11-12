from fastapi.testclient import TestClient

from subnet_calculator_sqa.api import app

client = TestClient(app)


def test_subnet_ok():
    r = client.get("/subnet", params={"ip": "192.168.10.37", "prefix": 26})
    assert r.status_code == 200
    assert r.json()["broadcast"] == "192.168.10.63"


def test_ip_salah_422():
    r = client.get("/subnet", params={"ip": "999.1.1.1", "prefix": 24})
    assert r.status_code == 422


def test_prefix_salah_422():
    r = client.get("/subnet", params={"ip": "10.0.0.1", "prefix": 40})
    assert r.status_code == 422