from fastapi.testclient import TestClient
from main import app

def test_health_and_openapi():
	client = TestClient(app)
	r = client.get('/health')
	assert r.status_code == 200
	assert r.json().get('status') == 'ok'
	ro = client.get('/openapi.json')
	assert ro.status_code == 200
	assert ro.json().get('openapi')