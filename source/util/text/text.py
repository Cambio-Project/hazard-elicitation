import random
from util.log import warning
from util.text.languages import LanguageConfig, TEXT


def text(text_id: int) -> str:
    if LanguageConfig.LANGUAGE not in TEXT:
        LanguageConfig.LANGUAGE = 'en'
        warning('Fallback to default language "en" since {} does not exist.'.format(LanguageConfig.LANGUAGE))

    if text_id in TEXT[LanguageConfig.LANGUAGE]:
        return TEXT[LanguageConfig.LANGUAGE][text_id]
    else:
        return 'NO TEXT ID "{}"'.format(text_id)


def random_text(text_id: int) -> str:
    result = text(text_id)
    return result[random.randint(0, len(result) - 1)]
