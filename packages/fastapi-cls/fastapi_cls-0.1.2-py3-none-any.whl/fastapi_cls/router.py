from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
    Any,
    Callable,
    Type,
    get_type_hints
)
from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.routing import APIRouter, APIRoute
from fastapi.encoders import DictIntStrAny, SetIntStr
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from fastapi_cls.view_maker import method_view


class ClassRouter(APIRouter):
    """
    Customize fastapi apirouter
    """
    # if not TYPE_CHECKING: # overwrite: get response_model from return hint by default.

    def add_method_route(
        self,
        path: str,
        cls: Type[Any],
        endpoint: Callable[..., Any],
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[Union[Set[str], List[str]]] = ["GET"],
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
        name: Optional[str] = None,
        route_class_override: Optional[Type[APIRoute]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None
    ) -> None:
        method_view(cls, endpoint)
        # print(getattr(endpoint,'__fastapi__view__'))
        # kwargs['dependencies'] = getattr(cls,'dependencies',[])
        return self.add_api_route(
            path,
            endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            route_class_override = route_class_override,
            callbacks=callbacks,
            openapi_extra=openapi_extra
            )

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[Union[Set[str], List[str]]] = ["GET"],
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
        name: Optional[str] = None,
        route_class_override: Optional[Type[APIRoute]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        if response_model is None:
            response_model = get_type_hints(endpoint).get("return")
        return super().add_api_route(
            path,
            endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            route_class_override = route_class_override,
            callbacks=callbacks,
            openapi_extra=openapi_extra
            )

    def add_resource(
        self,
        path: str,
        resource: Type[Any],
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[Union[Set[str], List[str]]] = ["GET"],
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
        name: Optional[str] = None,
        route_class_override: Optional[Type[APIRoute]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        methods: Set[str] = set([method.lower() for method in methods])
        for method in methods:
            meth = getattr(resource, method, None)
            assert meth is not None, 'Unimplemented method %r' % method
            self.add_method_route(
                path,
                resource,
                meth,
                response_model=response_model,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=response_model_exclude_unset,
                response_model_exclude_defaults=response_model_exclude_defaults,
                response_model_exclude_none=response_model_exclude_none,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                route_class_override = route_class_override,
                callbacks=callbacks,
                openapi_extra=openapi_extra
            )
        return
