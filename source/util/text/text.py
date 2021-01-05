import random

from util.text.languages import LanguageConfig, TEXT


def text(text_id: int):
    if LanguageConfig.LANGUAGE not in TEXT:
        LanguageConfig.LANGUAGE = 'en'
        # log: fallback to default language 'en'

    if text_id in TEXT[LanguageConfig.LANGUAGE]:
        return TEXT[LanguageConfig.LANGUAGE][text_id]
    else:
        return '<NO TEXT ID "{}">'.format(text_id)


def random_text(text_id: int):
    result = text(text_id)
    return result[random.randint(0, len(result) - 1)]
