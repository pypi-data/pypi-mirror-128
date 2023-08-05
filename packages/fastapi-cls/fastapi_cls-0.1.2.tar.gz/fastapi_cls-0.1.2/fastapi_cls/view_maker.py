import inspect
from typing import Any, Callable, List, Type, Union, get_type_hints

from fastapi import Depends
from pydantic.typing import is_classvar


VIEW_KEY = "__fastapi__view__"

def method_view(cls: Type[Any], method: Union[str,Callable]) ->  None:
    _class_view(cls)
    if isinstance(method, Callable):
        method = method.__name__
    _method_view(cls, method)


def class_methods_view(cls: Type[Any], methods: List[str]) ->  None:
    _class_view(cls)
    _method_view(cls,methods)


def _class_view(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` function is updated to set any class-annotated dependencies as instance attributes
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments should be passed to the initializer
    """
    if getattr(cls, VIEW_KEY, False):  # pragma: no cover
        return  # Already initialized   
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, VIEW_KEY, True)


def _method_view(cls: Type[Any], methods: List[str]) -> None:
    function_members = inspect.getmembers(cls, inspect.isfunction)
    for func_name, func in function_members:
        if func_name in methods:
            _update_endpoint_signature(cls, func)


def _update_endpoint_signature(cls: Type[Any], endpoint: Callable) -> None:
    """
    Update the endpoint signature to ensure FastAPI performs dependency injection properly.
    """
    if getattr(endpoint, VIEW_KEY, False):  # pragma: no cover
        return  # Already initialized        
    old_signature = inspect.signature(endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]
    new_first_parameter = old_first_parameter.replace(default=Depends(cls))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY) for parameter in old_parameters[1:]
    ]
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(endpoint, "__signature__", new_signature)
    setattr(endpoint, VIEW_KEY, True)