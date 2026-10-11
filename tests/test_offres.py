from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_creer_offre_persiste_et_apparait_dans_liste() -> None:
    # Création
    reponse_creation = client.post(
        "/offres/creer",
        data={"titre": "Développeur Python", "description": "Poste backend"},
        follow_redirects=False,
    )
    assert reponse_creation.status_code in (302, 303)

    # Vérification dans la liste
    reponse_liste = client.get("/offres")
    assert reponse_liste.status_code == 200
    contenu = reponse_liste.text
    assert "Développeur Python" in contenu
    assert "Poste backend" in contenu


def test_modifier_offre_persiste_apres_rechargement() -> None:
    # Créer une offre
    reponse_creation = client.post(
        "/offres/creer",
        data={"titre": "Data Analyst", "description": "Analyse de données"},
        follow_redirects=False,
    )
    assert reponse_creation.status_code in (302, 303)

    # Récupérer l'ID depuis la liste (dernier)
    reponse_liste = client.get("/offres")
    assert reponse_liste.status_code == 200
    import re

    matches = re.findall(r"/offres/(\d+)", reponse_liste.text)
    assert matches
    offre_id = matches[-1]

    # Modifier
    reponse_modif = client.post(
        f"/offres/{offre_id}/modifier",
        data={
            "titre": "Data Scientist Senior",
            "description": "ML et IA",
        },
        follow_redirects=False,
    )
    assert reponse_modif.status_code in (302, 303)

    # Recharger liste
    reponse_liste2 = client.get("/offres")
    assert reponse_liste2.status_code == 200
    assert "Data Scientist Senior" in reponse_liste2.text
    assert "ML et IA" in reponse_liste2.text


def test_detail_affiche_titre_et_description() -> None:
    # Créer une offre
    reponse_creation = client.post(
        "/offres/creer",
        data={"titre": "QA Engineer", "description": "Tests automatisés"},
        follow_redirects=False,
    )
    assert reponse_creation.status_code in (302, 303)

    # Récupérer l'ID (dernier)
    reponse_liste = client.get("/offres")
    import re

    matches = re.findall(r"/offres/(\d+)", reponse_liste.text)
    assert matches
    offre_id = matches[-1]

    # Détail
    reponse_detail = client.get(f"/offres/{offre_id}")
    assert reponse_detail.status_code == 200
    assert "QA Engineer" in reponse_detail.text
    assert "Tests automatisés" in reponse_detail.text
