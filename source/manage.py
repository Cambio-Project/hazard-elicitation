import os
from hazard_elicitation.settings import LANGUAGE_CODE, KEYS
from util.text.languages import LanguageConfig
from util.log import *


def setup():
    LanguageConfig.LANGUAGE = LANGUAGE_CODE
    info('"{}" set as default language.'.format(LanguageConfig.LANGUAGE))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hazard_elicitation.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    setup()
    if not KEYS.get('django_secret'):
        error('Check your "keys.json" file.')

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
