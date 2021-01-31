import os

from hazard_elicitation.settings import LANGUAGE_CODE, KEYS, TRACING
from util.text.languages import LanguageConfig
from util.log import *

if TRACING:
    from util.tracing import Tracer


def setup():
    # Language settings
    info('"{}" set as default language.'.format(LanguageConfig.LANGUAGE))
    LanguageConfig.LANGUAGE = LANGUAGE_CODE

    # Tracing
    if TRACING:
        info('Initialize Tracing.'.format(LanguageConfig.LANGUAGE))
        Tracer.setup("hazard")


def teardown():
    if TRACING:
        Tracer.tracer().close()


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

    info('Setup')
    setup()

    if not KEYS.get('django_secret'):
        error('Check your "keys.json" file.')
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        error('Check your "credentials.json" file.')

    execute_from_command_line(sys.argv)

    info('Teardown')
    teardown()


if __name__ == '__main__':
    main()
