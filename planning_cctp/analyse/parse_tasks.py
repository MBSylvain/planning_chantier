# Extraction des tâches et CPM


import re
import spacy

def extract_tasks_from_text(text: str):
	"""
	Détecte les tâches dans le texte PDF.
	- Repère les lots ("Lot X - ...")
	- Repère les actions (phrases avec verbe, durée, etc.)
	- Extrait la durée si présente (ex: "durée: 10 jours", "délai 2 semaines")
	"""
	nlp = spacy.load("fr_core_news_lg")
	tasks = []
	current_lot = ""
	id_counter = 1

	# Regex pour détecter les lots et les durées
	lot_regex = re.compile(r"Lot\s*\d+\s*-\s*.+", re.IGNORECASE)
	duree_regex = re.compile(r"(?:durée|délai)\s*:?\s*(\d+)\s*(jour|jours|semaine|semaines)", re.IGNORECASE)


	previous_task_id = None
	previous_task_title = None
	for line in text.splitlines():
		line = line.strip()
		if not line:
			continue
		# Détection du lot
		if lot_regex.match(line):
			current_lot = line
			continue

		# Extraction de la durée
		duree_jours = 5  # valeur par défaut
		m = duree_regex.search(line)
		if m:
			val, unit = m.groups()
			val = int(val)
			if "semain" in unit:
				duree_jours = val * 5  # 1 semaine = 5 jours ouvrés
			else:
				duree_jours = val

		# Utilisation de spaCy pour repérer les phrases d'action (verbe)
		doc = nlp(line)
		has_verb = any(tok.pos_ == "VERB" for tok in doc)
		if has_verb:
			# Détection dépendance textuelle simple
			deps = ""
			# Si la phrase contient "après" ou "dépend de", on relie à la tâche précédente
			if previous_task_id and ("après" in line.lower() or "dépend" in line.lower()):
				deps = str(previous_task_id)
			# Si la phrase mentionne explicitement une tâche précédente par mot-clé
			if previous_task_title and previous_task_title.lower() in line.lower():
				deps = str(previous_task_id)
			tasks.append({
				"id": id_counter,
				"lot": current_lot or "Lot ?",
				"intitule": line,
				"duree_jours": duree_jours,
				"deps": deps
			})
			previous_task_id = id_counter
			previous_task_title = line
			id_counter += 1

	# Fallback : si aucune tâche détectée, chaque ligne non vide devient une tâche
	if not tasks:
		for i, line in enumerate([l for l in text.splitlines() if l.strip()]):
			tasks.append({
				"id": i+1,
				"lot": "Lot ?",
				"intitule": line.strip(),
				"duree_jours": 5,
				"deps": ""
			})
	return tasks
