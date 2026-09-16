# Starter Kit v2 - Projet IA Bachelier 3 HEH
## Format 3 sprints sur 8 semaines (46h)

Template de projet prêt à l'emploi pour démarrer votre projet d'intégration IA.

## Ce qui est inclus

- **Backend FastAPI complet** avec :
  - Configuration Pydantic Settings + .env
  - Wrapper Gemini service (texte, structuré, streaming, multimodal)
  - SQLAlchemy + SQLite (avec exemple de modèle Conversation)
  - Endpoints chat (simple, structuré, streaming)
  - Endpoint multimodal (upload fichier)
  - CORS, rate limiting (slowapi), logs
- **Tests pytest** avec mocks et fixtures
- **Configuration qualité** : Ruff (linter) et MyPy (typage)
- **GitHub Action CI** : tests automatiques sur PR
- **Configuration Render** prête pour le déploiement
- **Templates** :
  - ADR (Architecture Decision Record)
- **README à compléter** par chaque groupe de 3

Le journal IA individuel et le `prompts.md` sont déjà fournis dans le dossier de votre projet (`05_materiel_complementaire/repo_template/`), adaptés à votre sujet : pas besoin de les reprendre ici.

## Quick Start

```bash
# 1. Cloner ce starter kit
git clone <url-template> mon-projet
cd mon-projet

# 2. Créer son environnement virtuel
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -e ".[dev]"

# 4. Configurer .env
cp .env.example .env
# Éditer .env et y mettre votre GEMINI_API_KEY

# 5. Initialiser la base de données
python -m backend.scripts.init_db

# 6. Lancer en dev
uvicorn backend.main:app --reload

# 7. Ouvrir http://localhost:8000/docs (Swagger UI auto-généré)
```

## Structure complète

```
starter_kit/
├── backend/
│   ├── main.py                    # Point d'entrée FastAPI
│   ├── config.py                  # Settings Pydantic
│   ├── database.py                # Setup SQLAlchemy
│   ├── models/
│   │   └── conversation.py        # Exemple modèle BDD
│   ├── services/
│   │   └── gemini_service.py      # Wrapper Gemini (4 méthodes)
│   ├── routers/
│   │   ├── chat.py                # Endpoints conversationnels
│   │   └── files.py               # Endpoints multimodaux
│   ├── schemas/
│   │   └── common.py              # Schémas Pydantic partagés
│   └── scripts/
│       └── init_db.py             # Initialisation BDD
├── adrs/
│   └── 0001-template.md           # Template ADR à compléter
├── tests/
│   ├── conftest.py
│   └── test_chat.py
├── .github/workflows/ci.yml       # CI GitHub Actions
├── .env.example                   # Template à copier en .env
├── .gitignore
├── pyproject.toml                 # Dépendances + config
├── render.yaml                    # Config déploiement Render
└── README.md                      # À compléter par votre groupe
```

## Commandes utiles

```bash
# Lancer les tests
pytest

# Linter le code
ruff check backend/
ruff format backend/

# Vérifier le typage
mypy backend/

# Lancer en mode debug
uvicorn backend.main:app --reload --log-level debug

# Initialiser/réinitialiser la BDD
python -m backend.scripts.init_db
```

## Déploiement sur Render

1. Push sur GitHub
2. Sur https://render.com, "New Web Service"
3. Connecter le repo
4. Build : `pip install -e .`
5. Start : `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Ajouter `GEMINI_API_KEY` dans Environment Variables
7. Deploy

(Le fichier `render.yaml` automatise une partie de cette config.)

## Frontend

Le starter ne fournit **pas** de frontend imposé. Choix libre :
- React (avec Vite)
- Vue 3 (avec Vite)
- HTML/CSS/JS vanilla pour rester simple
- Streamlit en Python pour aller très vite

**Recommandation** : si vous n'êtes pas sûrs, partez sur Vite + React ou Vue, déploiement Vercel en 2 clics.

## Convention de commits

Utilisez la convention "Conventional Commits" pour faciliter le CHANGELOG :

```
feat: nouvelle fonctionnalité
fix: correction de bug
docs: documentation
test: tests
refactor: refactoring sans changement fonctionnel
chore: tâches diverses (config, deps)
```

Exemple : `feat(chat): ajoute endpoint streaming`

## Tags de release

À chaque fin de sprint, taggez votre code :

```bash
git tag -a v0.1 -m "Sprint 1 : setup et premier appel IA"
git push origin v0.1
```

À la soutenance, le tag final doit être `v1.0`.
