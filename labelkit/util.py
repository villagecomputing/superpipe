from typing import TypedDict, Type, Dict, get_type_hints
from pydantic import create_model


def validate_dict(dict: Dict, type: Type[TypedDict]) -> Dict:
    field_definitions = get_type_hints(type)
    pydantic_model = create_model(
        type.__name__, **{k: (v, ...) for k, v in field_definitions.items()})
    pydantic_model.model_validate(dict)
