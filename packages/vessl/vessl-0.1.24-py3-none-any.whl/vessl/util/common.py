from datetime import datetime, timezone
from importlib import import_module

import timeago

from vessl.util import logger
from vessl.util.exception import ImportPackageError


def parse_time_to_ago(dt: datetime):
    if not dt:
        return "N/A"
    return timeago.format(dt, datetime.now(timezone.utc))


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def get_module(name, required=None):
    try:
        return import_module(name)
    except ImportError:
        msg = f"Error importing optional module {name}"
        if required:
            logger.warn(msg)
            raise ImportPackageError(f"{required}")
