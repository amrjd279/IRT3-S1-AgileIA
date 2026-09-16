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

## Étape 5 : Sortie structurée avec Pydantic

Objectif : extraire des entités d'un texte en JSON garanti conforme. La compétence la plus importante du cours.
1.	Dépliez POST /chat/sentiment dans Swagger UI, cliquez sur "Try it out".
```python 
class Sentiment(BaseModel):
    polarite: Polarite
    score_confiance: float = Field(ge=0, le=1)
    justification: str


@router.post("/sentiment", response_model=Sentiment)
async def analyser_sentiment(req: QuestionRequest, db: Session = Depends(get_db)):
    """Démo de sortie structurée Pydantic : analyse de sentiment d'un texte."""
    try:
        return gemini_service.generer_structure(
            f"Analyse le sentiment du texte suivant : {req.question}",
            schema=Sentiment,
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA : {e}") from e
```
#### Dans Swagger : 
1. Ouvre ``http://127.0.0.1:8000/docs``
2. Déplie ``POST /chat/sentiment``
3. Clique sur **Try it out**.
4. Utilise :
```python
{
  "question": "Le service est excellent et très rapide."
}
```
5. Clique sur **Execute**.
Réponse attendue :
```python
{
  "polarite": "positif",
  "score_confiance": 0.98,
  "justification": "Le texte exprime une satisfaction."
}
```
La sortie est contrainte par Pydantic : polarité limitée à trois valeurs, score entre 0 et 1, justification obligatoire. Vérification effectuée : 6 tests passent et la route apparaît bien dans OpenAPI.

2. Testez avec un texte, par exemple :
```python 
{
  "question": "Le service etait correct, sans plus."
}
```
* Le schéma réellement utilisé, dans backend/routers/chat.py :
```python 
class Polarite(str, Enum):
    positif = "positif"; negatif = "negatif"; neutre = "neutre"
 
class Sentiment(BaseModel):
    polarite: Polarite
    score_confiance: float = Field(ge=0, le=1)
    justification: str
```
* Test effectué avec : 
```python
{
  "question": "Le service etait correct, sans plus."
}
}
```
* Résultat HTTP 200 :
```python
{
  "polarite": "neutre",
  "score_confiance": 0.9,
  "justification": "L'expression 'correct, sans plus' indique un sentiment neutre."
}
```
La réponse respecte bien le schéma Pydantic : polarité valide, score compris entre 0 et 1, justification présente.

## À vous de jouer : Étendez le schéma vous même

Objectif : ajouter vous même un champ à un schéma Pydantic et en observer l'effet immédiat.

1.	Dans chat.py, ajoutez un champ à la classe Sentiment :
```python
langue_detectee: str | None = Field(
    default=None,
    description="Langue du texte analyse, en francais",
)
```
Swagger affiche maintenant ce champ comme optionnel. Les anciennes réponses restent compatibles avec ``langue_detectee: null``.

2. Sauvegardez : le serveur redémarre tout seul grâce à --reload. -> ``CTRL + S``

Le fichier est sauvegardé et le serveur tourne bien avec ```--reload```.
Après chaque modification suivie de ``Ctrl+S``, Uvicorn redémarre automatiquement. Vérification effectuée : ``/openapi.json`` répond ``HTTP 200`` et contient bien ``langue_detectee``.
```python 
  langue_detectee: str | None = Field(
        default=None,
        description="Langue du texte analyse, en francais",
    )
```

3. Relancez ``/chat/sentiment`` avec un texte dans une autre langue, vérifiez que le nouveau champ apparaît, rempli par le modèle

Test effectué avec un texte en anglais :
```python
{
  "question": "The service was correct, nothing more."
}
```
Réponse obtenue :
```python
{
  "polarite": "neutre",
  "score_confiance": 0.85,
  "justification": "L'expression indique une tonalité neutre.",
  "langue_detectee": "anglais"
}
```
## À vous de jouer : Cassez l'Enum et observez
Objectif : voir de vos propres yeux ce que l'Enum vous empêchait de voir.
#### Expérience réalisée puis annulée proprement.
* Avec temporairement : polarite: str
* Pydantic acceptait une valeur invalide :
```python 
{
  "polarite": "mitige",
  "score_confiance": 0.62,
  "justification": "Le texte est partagé."
}
```
* Swagger décrivait alors ``polarite`` comme une simple chaîne, sans restriction. L``Enum`` a ensuite été restauré : ``polarite: Polarite``
* Vérification : la valeur ``"mitige"`` est de nouveau rejetée par Pydantic.

1. Remplacez temporairement “polarite: Polarite” par “polarite: str” dans la classe Sentiment.
* Modification effectuée dans ``chat.py`` (Ligne 51-55) : 
```python
class Sentiment(BaseModel):
    polarite: str
```
Vérification réussie : une valeur comme ```"mitige"``` est maintenant acceptée.

2.	Relancez /chat/sentiment avec une phrase volontairement ambiguë, par exemple « Bof, sans plus, mais pas horrible non plus ».
```python
* La relance a finalement réussi avec :
{
  "question": "Bof, sans plus, mais pas horrible non plus"
}
```
Réponse HTTP ``200`` :
```python
{
  "polarite": "neutre",
  "score_confiance": 0.85,
  "justification": "Le texte exprime une opinion très mitigée et moyenne, sans enthousiasme ni rejet critique.",
  "langue_detectee": "français"
}
```