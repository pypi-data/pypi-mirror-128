from dataclasses import dataclass, Field, MISSING
from inspect import Parameter
from typing import Any, Optional, get_origin, get_args, Union


@dataclass(frozen=True)
class TargetField:

    name: str
    type: Any
    default: Optional[Any]

    @property
    def is_optional(self) -> bool:
        origin = get_origin(self.type)
        args = get_args(self.type)
        return origin is Union and type(None) in args

    @classmethod
    def from_parameter(cls, parameter: Parameter) -> 'TargetField':
        default = None if parameter.default is Parameter.empty else parameter.default
        return cls(
            name=parameter.name,
            type=parameter.annotation,
            default=default
        )

    @classmethod
    def from_field(cls, field: Field) -> 'TargetField':
        default = None if field.default is MISSING else field.default
        return cls(
            name=field.name,
            type=field.type,
            default=default
        )
