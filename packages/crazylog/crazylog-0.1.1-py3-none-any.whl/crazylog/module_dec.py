import types
import inspect
import typing


class ModuleDecorator:
    """Apply decorator to all objects in module"""

    def __init__(self, decorator: typing.Callable) -> None:
        self.decorator: typing.Callable = decorator
        self.functions: bool = True
        self.methods: bool = True
        self.classes: bool = True
        self.exclude_dunder: bool = True
        self.override_include: typing.List[str] = []

    def decorate_obj(
        self,
        module: types.ModuleType,
        name: str,
        obj: typing.Any,
    ):
        """Given a module and an object decorate the object.
        If the obj is a func or method decorate it. If the 
        `obj` is a class then decorate all its methods, excluding
        dunder methods.

        :param types.ModuleType module: [description]
        :param str name: [description]
        :param typing.Any obj: [description]
        """
        if isinstance(obj, (types.MethodType, types.FunctionType)):
            setattr(module, name, self.decorator(obj))
        elif inspect.isclass(obj):
            cls_objects = [m for m in dir(obj) if not m.startswith("__") and self.exclude_dunder]
            for cls_obj_name in cls_objects:
                cls_obj_attr = getattr(obj, cls_obj_name)
                setattr(obj, cls_obj_name, self.decorator(cls_obj_attr))

    def decorate_module(self, module: types.ModuleType):
        """Given a module, apply the decorator to all classes,
        methods and functions in given module.
        Users can fine-tune what to include by providing/editing instance vars.

        :param [type] module: [description]
        """
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.getmodule(obj) == module:
                self.decorate_obj(module, name, self.decorator, obj)

