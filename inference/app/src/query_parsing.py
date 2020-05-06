import re
from string import punctuation

from unidecode import unidecode


def clean(query):
    lowercased = query.lower()
    translator = str.maketrans(punctuation, " " * len(punctuation))
    without_punctuation = " ".join(lowercased.translate(translator).split())
    without_accents = unidecode(without_punctuation)
    return without_accents


def extract_years(cleaned_query):
    years = [
        int(token)
        for token in cleaned_query.split()
        if re.match("^\d{4}$", token)
    ]
    return years


def parse_query(query):
    cleaned = clean(query)
    years = extract_years(cleaned)
    return {
        "cleaned": cleaned,
        "years": years
    }
