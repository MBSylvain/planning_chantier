import pandas as pd
from analyse.parse_tasks import extract_tasks_from_text, build_schedule_dataframe
from datetime import date

def test_extract_tasks_basic():
    text = """
    Lot 1 - Maçonnerie
    Réaliser les fondations (durée: 10 jours).
    Poser les murs porteurs après fondations (délai 2 semaines).
    """
    tasks = extract_tasks_from_text(text)
    assert len(tasks) >= 2
    assert any("fondations" in t["intitule"].lower() for t in tasks)

def test_schedule_build():
    tasks = [
        {"id":1,"lot":"Lot 1 - Maçonnerie","intitule":"Réaliser fondations","duree_jours":10,"deps":""},
        {"id":2,"lot":"Lot 1 - Maçonnerie","intitule":"Poser murs porteurs","duree_jours":10,"deps":"1"},
    ]
    df = pd.DataFrame(tasks)
    sched = build_schedule_dataframe(df, start_date=date(2026,2,20))
    assert len(sched) == 2
    assert sched.iloc[1]["start"] >= sched.iloc[0]["finish"]
