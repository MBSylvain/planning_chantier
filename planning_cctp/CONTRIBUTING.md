# Bonnes pratiques de développement

## Commits
- Commits fréquents, messages clairs (feat:, fix:, docs:, refactor:, test:, chore:)
- Un commit = une idée/feature/correction

## Code
- Docstrings pour chaque fonction/classe
- Noms explicites pour variables/fonctions
- Commentaires pour toute logique complexe
- Respect du PEP8 (formatage auto avec Black)
- Limite de 88 caractères/ligne
- Imports organisés

## Tests
- Tests unitaires pour chaque module clé
- Lancer les tests avant chaque push

## Documentation
- README et doc à jour
- Expliquer les choix techniques importants

## Revue de code
- Relire son code avant commit/push
- Utiliser GitLens pour l’historique

## Sécurité & Qualité
- Jamais de secrets/mots de passe en clair
- Utiliser .env pour les variables sensibles
- Utiliser un linter (Pylance)

---

## Outils recommandés
- VS Code + extensions recommandées (voir .vscode/extensions.json)
- Black (formatage), Pylance (analyse), Autodocstring (docstrings)
