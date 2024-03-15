from typing import Union, Dict, Callable, TypeVar, Generic
from pydantic import BaseModel
import pandas as pd
from superpipe.steps.step import Step, StepResult
from superpipe.steps.utils import with_statistics

T = TypeVar('T', bound=BaseModel)


class CustomStep(Step, Generic[T]):
    """
    A convenience step for applying custom transformations. Use this to wrap any custom transformation function.

    Can be used to wrap LLM libs (langchain), API calls, custom data transformation, 3rd party libraries, etc.

    The output of the transformation must conform to a Pydantic model specified by `out_schema`.

    Methods:
        _run(row: Union[pd.Series, Dict]) -> Dict: Applies the transformation function to a single row of data and ensures the output matches the defined Pydantic model.
    """

    def __init__(self,
                 transform: Callable[[Union[pd.Series, Dict]], Dict],
                 out_schema: T,
                 name: str = None):
        """
        Initializes a new instance of the CustomStep class.

        Args:
            transform (Callable[[Union[pd.Series, Dict]], Dict]): The transformation function to apply to each row of data.

            out_schema (T): A Pydantic model that the output of the transform function should conform to.

            name (str, optional): An optional name for the step. Defaults to None.
        """
        super().__init__(name)
        self.transform = transform
        self.out_schema = out_schema

    def _run(self, row: Union[pd.Series, Dict]) -> Dict:
        """
        Applies the transformation function to a single row of data.

        This method ensures that the output of the transformation matches the fields defined in the Pydantic model specified by `out_schema`.

        Args:
            row (Union[pd.Series, Dict]): The data row to transform, which can be either a pandas Series or a dictionary.

        Returns:
            Dict: The transformed row, with keys corresponding to the fields defined in the `out_schema` Pydantic model.
        """
        transform = self.transform
        fields = self.out_schema.model_fields.keys()
        transformed, statistics = with_statistics(transform)(row)
        result = {f: transformed[f] for f in fields}
        return StepResult(fields=result, statistics=statistics)
