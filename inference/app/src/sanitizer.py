import re
from string import punctuation

import unidecode
from tqdm import tqdm

from .wiki import get_wikidata_candidates, get_wikidata_id


class TextSanitizer:
    def __init__(self, texts, progress=True):
        self.progress = progress
        self.texts = {
            i: {'raw': text, 'sanitized': text} for i, text in enumerate(texts)
        }

    def __getitem__(self, index):
        return self.texts[index]

    def _generate_tqdm_desc(self, function_name, n=21):
        clean_function_name = function_name.replace('_', ' ')
        whitespace = ' ' * (n - len(function_name))
        return clean_function_name + whitespace

    def _apply(func):
        def applied_func(self):
            if self.progress:
                desc = self._generate_tqdm_desc(func.__name__)
                for i, text in tqdm(self.texts.items(), desc=desc):
                    func(text)

            else:
                for i, text in self.texts.items():
                    func(text)

            return self

        return applied_func

    def redirect_duplicates(self):
        already_seen = {}
        desc = self._generate_tqdm_desc('redirect_duplicates')
        loop = tqdm(self.texts.items(), desc=desc)
        for i, text in loop:
            if text['sanitized'] in already_seen:
                text['redirect'] = already_seen[text['sanitized']]
            else:
                already_seen[text['sanitized']] = i
        return self

    @_apply
    def remove_punctuation(text):
        without_punctuation = text['sanitized'].translate(
            str.maketrans(punctuation, ' ' * len(punctuation))
        )
        text['sanitized'] = ' '.join(without_punctuation.split())
        return text

    @_apply
    def lowercase(text):
        text['sanitized'] = text['sanitized'].lower()
        return text

    @_apply
    def extract_years(text):
        for token in text['sanitized'].split():
            if re.match('^\d{4}$', token):
                if 'years' not in text:
                    text['years'] = []
                text['years'].append(int(token))
        return text

    @_apply
    def tokenise(text):
        text['tokens'] = text['sanitized'].split()
        return text

    @_apply
    def remove_accents(text):
        text['sanitized'] = unidecode.unidecode(text['sanitized'])
        return text

    @_apply
    def get_wikidata_id(text):
        # TODO : incorporate redirects
        query = text['sanitized']
        candidates = get_wikidata_candidates(query)

        if query in candidates:  # exact matching here
            try:
                wikidata_title = candidates[query]
                wikidata_id = get_wikidata_id(wikidata_title)
                text['wikidata'] = {'title': wikidata_title, 'id': wikidata_id}
            except KeyError:
                pass
                # TODO: logging here, everywhere

        return text

    def sanitized_texts(self):
        return [
            text['sanitized']
            for text in self.texts.values()
            if 'redirect' not in text
        ]

    def tokens(self):
        return [
            text['tokens']
            for text in self.texts.values()
            if 'redirect' not in text
        ]

    def wikidata_ids(self):
        return [
            text['wikidata']
            for text in self.texts.values()
            if (('wikidata' in text) and ('redirect' not in text))
        ]
