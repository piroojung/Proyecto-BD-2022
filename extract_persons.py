import spacy

from scrappers.antofagasta_enlalinea import textos as medio1


nlp = spacy.load("es_core_news_md")
persons = {}

for i, text in enumerate(medio1):
    persons[f"{i}"] = []
    doc = nlp(text)

    for ent in doc.ents:
        if (ent.label_ == "PER") and (" " in ent.text):
            persons[f"{i}"].append(ent.text)


