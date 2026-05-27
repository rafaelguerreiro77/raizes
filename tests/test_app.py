from fastapi.testclient import TestClient

from raizes.app import app

client = TestClient(app)
