from typing import Type, Any, Optional, TypeVar

T = TypeVar("T")


def implicit_cast(value: Any, target_type: Type[T]) -> T:
    # allow implicit int -> float cast
    if type(value) == int and target_type == float:
        value = float(value)

    if type(value) != target_type:
        raise TypeError(f"{type(value)} not equal to {target_type}")

    return value


def is_same_type(type1: Type[Any], type2: Type[Any]) -> bool:
    if type1 in (int, float) and type2 in (int, float):
        return True

    return type1 == type2
