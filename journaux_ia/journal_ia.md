# Journal IA

## Entree 1 - 17 septembre 2026

### Contexte
Test de l'endpoint `POST /chat/stream` du starter kit FastAPI pour observer l'affichage progressif d'une reponse Gemini.

### Demande envoyee
```json
{
  "question": "Raconte une courte histoire."
}
```

### Resultat
La reponse a ete affichee progressivement dans le terminal avec `curl.exe -N`, comme un effet machine a ecrire.

### Ce que j'ai accepte
J'ai conserve l'endpoint de streaming et son utilisation de `generate_content_stream`, car le resultat correspondait a l'objectif de l'exercice.

### Probleme rencontre et correction
Mes deux premiers essais avec le JSON directement dans PowerShell ont echoue avec une erreur `422 JSON decode error`. Les guillemets etaient mal transmis a `curl.exe`. J'ai corrige la commande en ecrivant temporairement le JSON dans un fichier, puis en utilisant `--data-binary @fichier.json`. Le test a ensuite fonctionne.

### Bilan
Le streaming est gere dans `backend/routers/chat.py` avec `StreamingResponse`, tandis que les morceaux sont produits par `generer_stream` dans `backend/services/gemini_service.py`. Cette verification m'a montre qu'un appel reussi depend aussi du formatage correct de la requete, pas seulement du prompt.
