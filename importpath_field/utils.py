import inspect
import sys
import types

import six

from .compat import import_string as _import_string


def is_class_method(klass, attr, value=None):
    """Test if a value of a class is class method.
    example::
        class MyClass(object):
            @classmethod
            def method(cls):
                ...
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in inspect.getmro(klass):
        if inspect.isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                if isinstance(binded_value, classmethod):
                    return True
    return False


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
    if obj is None:
        return None
    if isinstance(obj, types.ModuleType):
        return obj.__name__

    if hasattr(obj, '__self__'):
        # Maybe
        cls = obj.__self__
        if not is_class_method(cls, obj.__name__):
            raise ValueError('must be classmethod')
        return '.'.join([cls.__module__, cls.__name__, obj.__name__])
    return '.'.join([obj.__module__, obj.__name__])
