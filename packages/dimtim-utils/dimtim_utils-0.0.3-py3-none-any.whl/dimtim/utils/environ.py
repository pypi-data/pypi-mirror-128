from typing import Type, Union


def to_bool(value: Union[str, int, bool]) -> bool:
    if isinstance(value, str):
        return value.lower() in ('true', 't', '1')
    return bool(value)


def to_list(value: str, cast: Type = None) -> list[str]:
    result = []
    if isinstance(value, str):
        result = [v for v in value.split(',') if v]
    return [cast(v) for v in result] if callable(cast) else result
