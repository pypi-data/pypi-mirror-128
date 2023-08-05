import logging
import sys


log = logging.getLogger(__name__)


def _wrap_except_hook(old_except_hook):
    def fn(exc_type, exc_value, exc_tb):
        log.error("Unhandled exception: %s", exc_value)
        old_except_hook(exc_type, exc_value, exc_tb)

    return fn


def set_except_hook():
    sys.excepthook = _wrap_except_hook(sys.excepthook)
