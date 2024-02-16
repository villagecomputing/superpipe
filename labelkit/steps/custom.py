from typing import Union, Dict, Callable
import pandas as pd
from .step import Step, T


class CustomStep(Step):
    def __init__(self,
                 out_model: T,
                 transform: Callable[[Union[pd.Series, Dict]], T],
                 name: str = None):
        super().__init__(out_model, name, transform=transform)

    def apply(self, data: Union[pd.DataFrame, Dict]):
        fields = self.out_model.model_fields.keys()
        transform = self.params.get('transform')
        if isinstance(data, pd.DataFrame):
            transformed_series = data.apply(transform, axis=1)
            for field in fields:
                data[field] = transformed_series.apply(lambda x: x[field])
        else:
            transformed: T = transform(data)
            for field in fields:
                data[field] = transformed.model_dump()[field]
        return data
