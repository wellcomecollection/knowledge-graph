import json

import numpy as np

from src.elastic import get_concepts_data, get_elasticsearch_client
from src.sanitiser import TextSanitiser

with open('./config.json') as json_file:
    config = json.load(json_file)

es_client = get_elasticsearch_client(config)
results = get_concepts_data(es_client)

subjects = [
    result['_source']['label']
    for result in results
    if 'fromSubjects' in result['_source']
]

some_subjects = np.random.choice(subjects, 500)

sanitised = (
    TextSanitiser(some_subjects)
    .remove_punctuation()
    .remove_accents()
    .lowercase()
    .tokenise()
    .extract_years()
    .redirect_duplicates()
)

print(sanitised.sanitised_texts())
