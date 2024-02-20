from typing import Union, Dict
import pandas as pd


class Step():
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__

    def update_params(self, params: Dict):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        raise NotImplementedError

    def apply(self, data: Union[pd.DataFrame, Dict]):
        if isinstance(data, pd.DataFrame):
            new_fields = data.apply(
                lambda x: pd.Series(self._apply(x)), axis=1)
            data[new_fields.columns] = new_fields
        else:
            data.update(self._apply(data))
        return data
