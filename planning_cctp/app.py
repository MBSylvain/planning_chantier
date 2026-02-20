# Interface principale Streamlit

import streamlit as st


def try_import(module_name: str):
	try:
		return __import__(module_name, fromlist=["*"])
	except Exception:
		return None


st.title("Analyse CCTP/CCAP → Planning (PDF → Excel/MS Project)")

st.write("""
1. Upload un PDF CCTP/CCAP
2. Analyse automatique des tâches et dépendances
3. Édition manuelle des tâches
4. Export planning Excel ou MS Project XML
""")

uploaded_file = st.file_uploader("Uploader un PDF CCTP/CCAP", type=["pdf"])

def show_missing_deps_message(missing):
	st.warning("Dépendances manquantes : " + ", ".join(missing))
	st.info("Exécutez par exemple : `py -3 -m pip install streamlit pandas pdfplumber pytesseract pillow spacy`")


if uploaded_file is not None:
	st.info("Analyse du PDF en cours...")
	file_bytes = uploaded_file.read()

	extract_mod = try_import("analyse.extract_pdf")
	parse_mod = try_import("analyse.parse_tasks")
	pd = try_import("pandas")

	missing = []
	if extract_mod is None:
		missing.append("analyse.extract_pdf (pdfplumber/pytesseract)")
	if parse_mod is None:
		missing.append("analyse.parse_tasks (spacy)")
	if pd is None:
		missing.append("pandas")

	if missing:
		show_missing_deps_message(missing)
		# Provide a simple fallback: show raw text if possible
		if extract_mod is not None:
			try:
				text = extract_mod.extract_text_from_pdf(file_bytes)
				st.text_area("Texte extrait (mode dégradé)", text, height=300)
			except Exception as e:
				st.error(f"Impossible d'extraire le texte : {e}")
	else:
		try:
			text = extract_mod.extract_text_from_pdf(file_bytes)
			tasks = parse_mod.extract_tasks_from_text(text)
			if tasks:
				df_tasks = pd.DataFrame(tasks)
			else:
				st.warning("Aucune tâche détectée dans le PDF.")
				df_tasks = None
		except Exception as e:
			st.error(f"Erreur durant l'analyse : {e}")
			df_tasks = None

		if df_tasks is None:
			st.caption("(Aucune tâche à éditer tant qu'un PDF n'est pas analysé)")
		else:
			st.subheader("📝 Éditeur de tâches")
			st.info("Modifiez les champs puis cliquez sur 'Valider les modifications'.")
			edited_df = st.data_editor(
				df_tasks,
				column_config={
					"id": st.column_config.Column(disabled=True),
					"lot": st.column_config.TextColumn("Lot"),
					"intitule": st.column_config.TextColumn("Intitulé de la tâche"),
					"duree_jours": st.column_config.NumberColumn("Durée (jours)", min_value=1),
					"deps": st.column_config.TextColumn("Dépendances (id séparés par ,)")
				},
				num_rows="dynamic",
				use_container_width=True,
				key="editor"
			)
			if st.button("Valider les modifications"):
				st.success("Tâches mises à jour !")
				st.write(edited_df)


st.subheader("⬇️ Export")
st.write("(À venir : export Excel / MS Project XML)")
