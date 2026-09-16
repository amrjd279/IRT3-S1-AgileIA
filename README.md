# IRT3-S1-AgileIA

## À vous de jouer : Lisez le vrai code qui a tourné

Objectif : ouvrir le fichier qui a réellement exécuté votre appel, pas seulement l'exemple simplifié du cours.

* Ouvrez backend/services/gemini_service.py dans votre éditeur : c'est ce fichier, pas la théorie du matin, qui a réellement appelé Gemini quand vous avez cliqué Execute.

* Question 1 : quel modèle Gemini est utilisé par défaut, et où est-ce configuré (indice : backend/config.py) ?
1. Le modèle Gemini utilisé par défaut est gemini-3.6-flash.
### Il est configuré dans config.py (ligne 13) : default_model: str = "gemini-3.6-flash"
### Puis utilisé dans gemini_service.py (ligne 58) : model = model or settings.default_model

* Question 2 : que se passe-t-il si l'appel à Gemini échoue, dans la fonction generer_texte ?
### Si l’appel à Gemini échoue dans ``generer_texte``, cette fonction ne capture pas l’erreur : l’exception remonte directement.

POURQUOI CETTE ÉTAPE : le code des slides est volontairement simplifié pour l'explication. Le vrai fichier gère aussi les erreurs et la configuration par défaut : savoir le retrouver et le lire vous servira tout le semestre, bien au-delà de cette démo."

---

## À vous de jouer : Écrivez votre propre script

Objectif : reprendre en main le code que vous venez de lire, en écrivant vous-même sa version la plus nue, sans FastAPI ni Swagger autour.

1.	Créez un nouveau fichier scripts/appel_direct.py (créez le dossier scripts/ s'il n'existe pas encore).
# scripts/appel_direct.py 
```python
from google import genai
from backend.config import settings
 
client = genai.Client(api_key=settings.gemini_api_key)
response = client.models.generate_content(
    model=settings.default_model,
    contents="Explique le RGPD en 3 phrases.",
)
print(response.text)
```

2. Lancez-le avec python ``scripts/appel_direct.py``, sans uvicorn ni navigateur : c'est un script Python ordinaire, pas un endpoint.
#### Le script a été exécuté directement avec succès, sans Uvicorn ni navigateur. Gemini a répondu avec une explication du RGPD en trois phrases.

3. Comparez avec backend/services/gemini_service.py, ouvert à l'exercice précédent : c'est la même logique, juste sans la couche FastAPI autour.
* création du client Gemini avec ``settings.gemini_api_key`` -> ``gemini_api_key: str``
* utilisation de ``settings.default_model`` -> ``default_model: str = "gemini-3.6-flash"``
* appel à ``client.models.generate_content(...)``
* lecture de ``response.text`` -> ``response = _client.models.generate_content(model=model, contents=prompt, config=config)``
