import uvicorn
from app.api.load_app import app

# Ce fichier est le point d'entrée pour le développement local uniquement.
# Le serveur de production (UWSGI sur Alwaysdata) importe directement l'objet `app`
# depuis `api.load_app` et n'exécute pas ce code.

if __name__ == "__main__":
    # Utiliser une chaîne de caractères est une pratique courante et permet d'activer
    # le rechargement automatique (`reload=True`), ce qui est très pratique en développement.
    uvicorn.run("api.load_app:app", host="127.0.0.1", port=5000, reload=True)