import inspect
import sys
import types

import six

from .compat import import_string as _import_string
from .inspect_mate import is_class_method, is_static_method


def import_string(path):
    try:
        return _import_string(path)
    except ModuleNotFoundError:
        # Maybe is class attribute
        class_path, attr_name = path.rsplit('.', 1)
        _cls = _import_string(class_path)
        try:
            return getattr(_cls, attr_name)
        except AttributeError:
            msg = 'Class "%s" does not define a "%s" attribute/class' % (
                class_path, attr_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def get_path(obj):
    if isinstance(obj, types.ModuleType):
        return obj.__name__

    if hasattr(obj, '__self__'):
        # Maybe
        cls = obj.__self__
        if not is_class_method(cls, obj.__name__):
            raise ValueError('must be classmethod')
        return '.'.join([cls.__module__, cls.__name__, obj.__name__])
    return '.'.join([obj.__module__, obj.__name__])
