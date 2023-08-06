from dataclasses import is_dataclass, fields
from functools import partial
from inspect import signature
from typing import Any, TypeVar, List, Set, Optional, Dict

from parametric_builder.target_field import TargetField

TargetClass = TypeVar('TargetClass')


class Builder:
    """@DynamicAttrs"""
    NEWLINE = "\n"

    def __init__(self, target: TargetClass, **kwargs: Any) -> None:
        self.target = target
        self._kwargs = kwargs
        self._dir = self.field_names
        for field in self.fields:
            self._prepare_field(field)

    @property
    def fields(self) -> List[TargetField]:
        if is_dataclass(self.target):
            return list(map(TargetField.from_field, fields(self.target)))
        else:
            _params = signature(self.target).parameters.values()
            return list(map(TargetField.from_parameter, _params))

    @property
    def field_names(self) -> Set[str]:
        return {field.name for field in self.fields}

    def __contains__(self, item: str) -> bool:
        return item in self.field_names

    def __getitem__(self, item: str) -> Optional[Any]:
        return getattr(self, item)

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self:
            setattr(self, key, value)
        else:
            raise AttributeError(
                f"Target class, {self.target.__name__}, has no field: {key}\n"
                f"Available fields:\n {self.NEWLINE.join(self.field_names)}"
            )

    def __dir__(self) -> List[str]:
        return list(self._dir)

    def _prepare_field(self, field: TargetField) -> None:
        self._init_field_value(field)
        self._init_setter(field)

    def _init_field_value(self, field: TargetField) -> None:
        if field.name in self._kwargs:
            value = self._kwargs[field.name]
        elif field.default is not None:
            value = field.default
        else:
            value = None
        setattr(self, field.name, value)

    def _init_setter(self, field: TargetField) -> None:
        setter = f"with_{field.name}"
        setattr(self, setter, partial(self._with, field_name=field.name))

    def _with(self, value: Any, field_name: str) -> 'Builder':
        setattr(self, field_name, value)
        return self

    def build(self, **kwargs: Any) -> TargetClass:
        constructor_args = self._prepare_args(**kwargs)
        return self.target(**constructor_args)

    def _prepare_args(self, **kwargs: Any) -> Dict[str, Any]:
        return {
            field.name: self._assign_value(field, **kwargs)
            for field in self.fields
        }

    def _assign_value(self, field: TargetField, **kwargs: Any) -> Any:
        if field.name in kwargs:
            return kwargs[field.name]
        elif getattr(self, field.name) is not None:
            return getattr(self, field.name)
        elif field.default is not None:
            return field.default
        elif field.is_optional:
            return None
        else:
            raise ValueError(f"Required field [{field.name}] not assigned!")
