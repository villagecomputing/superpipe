from typing import Union, Dict, TypeVar, Generic
from pydantic import BaseModel
import pandas as pd

T = TypeVar('T', bound=BaseModel)


class Step(Generic[T]):
    def __init__(self,
                 out_model: T,
                 name: str = None,
                 **params):
        self.name = name or self.__class__.__name__
        self.out_model = out_model
        self.params = params

    def update_params(self, params):
        self.params.update(params)

    def apply(self, data: Union[pd.DataFrame, Dict]):
        raise NotImplementedError
