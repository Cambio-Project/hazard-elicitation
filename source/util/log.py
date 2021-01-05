import sys
import traceback


def tb(e: BaseException) -> str:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return 'Exception: "{}" of type "{}" for object "{} ({})"\n{}'.format(
        e, exc_type, exc_tb, type(exc_tb), traceback.format_exc())
