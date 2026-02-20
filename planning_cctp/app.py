# Interface principale Streamlit

import streamlit as st



import pandas as pd
from analyse.extract_pdf import extract_text_from_pdf
from analyse.parse_tasks import extract_tasks_from_text

st.title("Analyse CCTP/CCAP → Planning (PDF → Excel/MS Project)")

st.write("""
1. Upload un PDF CCTP/CCAP
2. Analyse automatique des tâches et dépendances
3. Édition manuelle des tâches
4. Export planning Excel ou MS Project XML
""")

uploaded_file = st.file_uploader("Uploader un PDF CCTP/CCAP", type=["pdf"])

df_tasks = None
if uploaded_file is not None:
	st.info("Analyse du PDF en cours...")
	file_bytes = uploaded_file.read()
	text = extract_text_from_pdf(file_bytes)
	tasks = extract_tasks_from_text(text)
	if tasks:
		df_tasks = pd.DataFrame(tasks)
	else:
		st.warning("Aucune tâche détectée dans le PDF.")

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
