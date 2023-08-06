import logging
import sys
import types
from contextlib import ContextDecorator
from datetime import datetime
from pprint import pformat
from types import FunctionType, MethodType
from typing import Callable, Dict, List

from crazylog.module_dec import ModuleDecorator


def log_like_crazy(frame, event, arg):
    """At each line that is executed, log
    the package.class line num and actual line of code being executed.
    In addition log all globals and locals of frame.
    # TODO make this plugin architecture. Allowing, for N decorators to be applied in trace.
    
    :param [type] frame: [description]
    :param [type] event: [description]
    :param [type] arg: [description]
    :return [type]: [description]
    """
    import linecache

    if event in ["line", "return"]:
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)

        logging.debug(f"{name}, {lineno}, {line.rstrip()}")
        logging.debug(pformat(frame.f_globals))
        logging.debug(pformat(frame.f_locals))
    return log_like_crazy


class CrazyLogger(ContextDecorator):
    """
    CrazyLogger logs all globals, locals and execution steps of everthing
    under the context of CrazyLogger.
    CrazyLogger can be used either as a context manager, a decorator, a metaclass
    or can be dynamically attached at runtime to modules.
    In those modules it can be used just for functions just for classes or both.

    .. code-block :: python

       def foo():
           print('inside foo')

       with CrazyLogger() as crazy:
           foo()
        
       # Alternatively, run it exclusively on a collection of classes
       class MyClass:
           pass

       with CrazyLogger() as crazy:
           crazy.exclusively = [MyClass]
           foo()   

    :param type ContextDecorator: Inherit from ContextDecorator so this context manager can be used as a decorator.
    """

    def __init__(
        self,
        func: Callable = log_like_crazy,
        log_config: Dict[str, str] = None,
        *arg,
        **kwargs,
    ):
        """Initialize CrazyLogger

        :param Callable func: a function to be executed at each execution step, defaults to log_like_crazy
        :param Dict[str, str] log_config: standard log config, defaults to None
        """
        self.func = func
        self.globals = True
        self.locals = True
        self._exclusively: List[object] = []

        if log_config:
            logging.basicConfig(**log_config)
        else:
            logging.basicConfig(
                filename=f"{__name__}.{datetime.utcnow():%Y%m%d_%S}.log",
                filemode="w",
                encoding="utf-8",
                level=logging.DEBUG,
            )

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

    @staticmethod
    def apply(module_str: str, functions: bool = True, classes: bool = True) -> bool:
        """`apply` is intended to be used when you want to attach CrazyLogger
        at the module level only.

        .. code-block:: python

           # package/my_module.py
           from crazy_logger import CrazyLogger
           CrazyLogger.apply(__name__)

           # Alternatlivy, it can be beneficial to only use CrazyLogger
           # when debugging. A common case is to have a variable DEBUG=True/False.
           # In the following case, `apply` will only have any affect if DEBUG is True.

           # package/my_module.py
           from crazy_logger import CrazyLogger
           from settings import DEBUG
           CrazyLogger.apply(__name__, DEBUG, DEBUG)

        :param str module: the module to apply CrazyLogger to
        :param bool functions: add CrazyLogger to all functions in `module`, defaults to True
        :param bool classes: add CrazyLogger to all classes and methods in `module`, defaults to True
        :return bool: boolean success value
        """
        import importlib

        module: types.ModuleType = importlib.import_module(module_str)
        mod_dec: ModuleDecorator = ModuleDecorator(CrazyLogger())
        if functions and classes:
            mod_dec.decorate_module(module)
        elif functions:
            pass
        elif classes:
            pass
        else:
            pass
        return functions or classes

    @property
    def exclusively(self):
        return self._exclusively

    @exclusively.setter
    def exclusively(self, exclusively: List[object]):
        self._exclusively = exclusively


class CrazyLoggerMeta(type):
    """Attach this metaclass to any class that needs crazy logging.

    .. code-block :: python

       class Pizza(metaclass=CrazyLoggerMeta):
           def __init__(self, ...):
               pass
    """

    def __new__(metacls, cls, bases, classdict):
        new_cls = super().__new__(metacls, cls, bases, classdict)

        for attr_name, attr_val in classdict.items():
            if isinstance(attr_val, (FunctionType, MethodType)):
                setattr(new_cls, attr_name, CrazyLogger()(attr_val))
        return new_cls
