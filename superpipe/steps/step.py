from typing import Union, Dict
import pandas as pd
from superpipe.config import is_dev


class Step():
    """
    A base class for defining a single step in a data-transformation pipeline.

    This class is designed to be subclassed for specific tasks. It provides
    a framework for applying transformations to pandas DataFrame objects or dictionaries.

    Attributes:
        name (str): The name of the step. Defaults to the class name if not provided.

    Methods:
        update_params(params): Updates the step's parameters with values from a dictionary.
        _apply(row): Abstract method for applying the step's transformation to a single row.
        apply(data): Applies the step's transformation to a DataFrame or dictionary.
    """

    def __init__(self, name: str = None):
        """
        Initializes a new instance of the Step class.

        Args:
            name (str, optional): The name of the step. Defaults to the class name if None.
        """
        self.name = name or self.__class__.__name__

    def update_params(self, params: Dict):
        """
        Updates the step's parameters with values from a dictionary.

        Args:
            params (Dict): A dictionary of parameters to update.
        """
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
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

    def apply(self, data: Union[pd.DataFrame, Dict], verbose=True):
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
                new_fields = pd.DataFrame(
                    [self._apply(row) for _, row in tqdm(data.iterrows(), total=len(data))])
            else:
                new_fields = pd.DataFrame(
                    [self._apply(row) for _, row in data.iterrows()])
            data[new_fields.columns] = new_fields
        else:
            data.update(self._apply(data))
        return data
