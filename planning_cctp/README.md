# Analyse CCTP/CCAP → Planning (PDF → Excel/MS Project)

Application **Streamlit** 100 % locale (hors-ligne) qui :
- extrait le texte d'un PDF (CCTP/CCAP),
- détecte des **tâches** et **dépendances**,
- calcule un **planning** (CPM simplifié + chemin critique),
- exporte en **Excel (Gantt)** et **MS Project XML**.

## Prérequis
- Python 3.10+
- (Optionnel OCR) Tesseract installé

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Lancer l'app

```bash
streamlit run app.py
```

## Structure

*   `analyse/` : extraction PDF, NLP, parsing des tâches
*   `generation/` : export Excel & MS Project
*   `tests/` : tests unitaires
*   `data/` : exports et temporaires

## Roadmap

*   Édition manuelle des tâches
*   Jours ouvrés & calendriers
*   IA locale (CamemBERT/Mistral) pour dépendances
