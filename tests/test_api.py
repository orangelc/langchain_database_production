from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query", json={"question": "¿Cuántos clientes hay?"})
    assert response.status_code == 200
    assert "answer" in response.json()
