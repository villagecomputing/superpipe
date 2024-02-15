from pydantic import BaseModel
from typing import get_origin, get_args, get_type_hints
import inspect


def describe_pydantic_model(model_class: BaseModel, indent: str = ""):
    model_description = ""
    fields = model_class.model_fields
    for field_name, field_info in fields.items():
        field_type = get_type_hints(model_class)[field_name]
        field_type_parent = get_origin(field_type)
        description = field_info.description or ""

        # TODO: handle more types.
        # Currently only handles lists of BaseModels, lists of primitives, BaseModels, and primitives)
        if field_type_parent is list:
            element_type = get_args(field_type)[0]
            if inspect.isclass(element_type) and issubclass(element_type, BaseModel):
                model_description += f"{indent}- {field_name} (list): {description} \n Each item in this list should follow the structure:\n"
                model_description += describe_pydantic_model(
                    element_type, indent + "\t")
            else:
                model_description += f"{indent}- {field_name} (list): {description} \n Each item in this list should be of type {element_type.__name__}\n"
        elif inspect.isclass(field_type) and issubclass(field_type, BaseModel):
            model_description += f"{indent}- {field_name} (obj): {description} \n This should follow the structure:\n"
            model_description += describe_pydantic_model(
                field_type, indent + "\t")
        else:
            model_description += f"{indent}- {field_name} ({field_type.__name__}): {description}\n"
    return model_description
