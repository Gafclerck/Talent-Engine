from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sante_renvoie_ok() -> None:
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.json() == {"statut": "ok"}
