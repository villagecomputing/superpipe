from typing import Union, Dict
from pydantic import BaseModel
import pandas as pd
from superpipe.config import is_dev


class StepStatistics(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0
    input_cost: float = 0.0
    output_cost: float = 0.0


class StepRowStatistics(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    success: bool = True
    latency: float = 0.0
    input_cost: float = 0.0
    output_cost: float = 0.0


class StepResult(BaseModel):
    fields: Dict
    statistics: StepRowStatistics


class Step():
    """
    A base class for defining a single step in a data-transformation pipeline.

    This class is designed to be subclassed for specific tasks. It provides
    a framework for applying transformations to pandas DataFrame objects or dictionaries.

    Attributes:
        name (str): The name of the step. Defaults to the class name if not provided.

    Methods:
        update_params(params): Updates the step's parameters with values from a dictionary.
        _run(row): Abstract method for applying the step's transformation to a single row.
        run(data): Applies the step's transformation to a DataFrame or dictionary.
    """

    def __init__(self, name: str = None):
        """
        Initializes a new instance of the Step class.

        Args:
            name (str, optional): The name of the step. Defaults to the class name if None.
        """
        self.name = name or self.__class__.__name__
        self.reset_statistics()

    def reset_statistics(self):
        """
        Resets the statistics for the step.
        """
        self.statistics = StepStatistics()

    def _update_statistics(self, statistics: StepRowStatistics):
        """
        Updates the statistics based on the response from the LLM.

        Args:
            response (LLMResponse): The response from the LLM.
        """
        self.statistics.input_tokens += statistics.input_tokens
        self.statistics.output_tokens += statistics.output_tokens
        self.statistics.total_latency += statistics.latency
        if statistics.success:
            self.statistics.num_success += 1
        else:
            self.statistics.num_failure += 1
        self.statistics.input_cost += statistics.input_cost
        self.statistics.output_cost += statistics.output_cost

    def update_params(self, params: Dict):
        """
        Updates the step's parameters with values from a dictionary.
        Also resets the step's statistics.

        Args:
            params (Dict): A dictionary of parameters to update.
        """
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.reset_statistics()

    def _run(self, row: Union[pd.Series, Dict]) -> StepResult:
        """
        Abstract method for applying the step's transformation to a single row.

        This method should be implemented by subclasses to define the specific transformation.

        Args:
            row (Union[pd.Series, Dict]): The data row to transform.

        Returns:
            Dict: The transformed row as a dictionary.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError

    def run(self, data: Union[pd.DataFrame, Dict], verbose=True):
        """
        Applies the step's transformation to a DataFrame or dictionary.

        If the input is a DataFrame, the transformation is applied to each row, and the result
        is assigned back to the DataFrame. If the input is a dictionary, it is directly updated
        with the result of the transformation.

        Can be overridden in subclasses to provide custom behavior.

        Args:
            data (Union[pd.DataFrame, Dict]): The data to transform.

        Returns:
            Union[pd.DataFrame, Dict]: The transformed data.
        """
        if verbose:
            print(f"Running step {self.name}...")
        if isinstance(data, pd.DataFrame):
            if verbose and is_dev:
                from tqdm import tqdm
                results = [self._run(row) for _, row in tqdm(
                    data.iterrows(), total=len(data))]
            else:
                results = [self._run(row) for _, row in data.iterrows()]
            for r in results:
                self._update_statistics(r.statistics)
            new_fields = pd.DataFrame([r.fields for r in results])
            data[new_fields.columns] = new_fields
        else:
            result = self._run(data)
            self._update_statistics(result.statistics)
            data.update(result.fields)
        return data
