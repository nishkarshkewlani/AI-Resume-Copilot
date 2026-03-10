import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(jd_text):

    doc = nlp(jd_text)

    keywords = []

    for token in doc:

        if token.pos_ in ["NOUN","PROPN"]:
            keywords.append(token.text.lower())

    return list(set(keywords))