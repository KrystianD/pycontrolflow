import typing
from typing import Type, Any, Optional, TypeVar, Dict, List

T = TypeVar("T")


def implicit_cast(value: Any, target_type: Type[T]) -> T:
    # allow implicit int -> float cast
    if isinstance(value, int) and target_type == float:
        value = float(value)

    if not isinstance(value, target_type):
        raise TypeError(f"{type(value)} not equal to {target_type}")

    return value


def is_same_type(type1: Type[Any], type2: Type[Any]) -> bool:
    if type1 in (int, float) and type2 in (int, float):
        return True

    return type1 == type2


def _get_generic_args_internal(typing_obj: Any, expected_class: Any, args_map: Optional[Dict[Any, Any]] = None) -> \
        Optional[List[Any]]:
    if args_map is None:
        args_map = {}

    obj = typing.get_origin(typing_obj) or typing_obj
    if obj is None:
        return None

    class_args = [args_map.get(x, x)
                  for x in typing.get_args(typing_obj)]  # get args and replace with passed mapping if exists

    if obj == expected_class:
        return class_args

    __orig_bases__ = getattr(obj, "__orig_bases__", None)
    if __orig_bases__ is None:
        return None

    generic_classes = [x for x in __orig_bases__ if typing.get_origin(x) == typing.Generic]
    if len(generic_classes) == 0:
        other_base_classes = obj.__orig_bases__
        args_map = None
    else:
        generic_cls = generic_classes[0]
        other_base_classes = [x for x in __orig_bases__ if typing.get_origin(x) != typing.Generic]
        generic_args = typing.get_args(generic_cls)
        assert len(class_args) == len(generic_args)

        args_map = {ga: ca for ca, ga in zip(class_args, generic_args)}

    for base_cls in other_base_classes:
        v = _get_generic_args_internal(base_cls, expected_class, args_map)
        if v is not None:
            return v

    return None


def get_generic_args_for_obj(obj: Any, expected_class: Any) -> List[Any]:
    typing_cls = getattr(obj, "__orig_class__", obj)
    res = _get_generic_args_internal(typing_cls, expected_class, {})
    if res is None:
        raise TypeError("no generic type")
    return res


__all__ = [
    "implicit_cast",
    "is_same_type",
    "get_generic_args_for_obj",
]
