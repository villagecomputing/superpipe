from typing import Union, Dict, Callable, TypeVar, Generic, TypedDict
from pydantic import BaseModel
import pandas as pd
from .step import Step
from ..util import validate_dict

T = TypeVar('T', bound=BaseModel)


class CustomStepParams(TypedDict):
    transform: Callable[[Union[pd.Series, Dict]], Dict]


class CustomStep(Step, Generic[T]):
    def __init__(self,
                 params: CustomStepParams,
                 out_model: T,
                 name: str = None):
        super().__init__(name)
        validate_dict(params, CustomStepParams)
        self.out_model = out_model
        self.params = params

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        transform = self.params['transform']
        fields = self.out_model.model_fields.keys()
        transformed = transform(row)
        return {
            field: transformed[field] for field in fields
        }
