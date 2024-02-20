from typing import Union, Dict, Callable, TypeVar, Generic, TypedDict
from pydantic import BaseModel
import pandas as pd
from .step import Step

T = TypeVar('T', bound=BaseModel)


class CustomStepParams(TypedDict):
    transform: Callable[[Union[pd.Series, Dict]], Dict]


class CustomStep(Step, Generic[T]):
    def __init__(self,
                 transform: Callable[[Union[pd.Series, Dict]], Dict],
                 out_schema: T,
                 name: str = None):
        super().__init__(name)
        self.transform = transform
        self.out_schema = out_schema

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        transform = self.transform
        fields = self.out_schema.model_fields.keys()
        transformed = transform(row)
        return {
            field: transformed[field] for field in fields
        }
