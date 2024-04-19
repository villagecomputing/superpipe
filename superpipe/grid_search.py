import itertools
import json
import os
import pandas as pd
from typing import Dict, List
from superpipe.pipeline import Pipeline
from superpipe.util import df_apply_gradients


class GridSearch:
    """
    Implements a grid search over a specified parameter grid for a given pipeline.

    Attributes:
        pipeline (Pipeline): The pipeline object on which the grid search is performed.
        params_list (list): A list of dictionaries, each representing a unique combination of parameters to be tested.
        results (pd.DataFrame or None): A DataFrame containing the results of the grid search once applied. Initially set to None.
    """

    def __init__(self, pipeline: Pipeline, params_grid: Dict):
        """
        Initializes the GridSearch object with a pipeline and a parameter grid.

        Args:
            pipeline (Pipeline): The pipeline object to perform the grid search on.
            params_grid (dict): A dictionary where keys are step names and values are dictionaries of parameter names to lists of possible values.
        """
        self.pipeline = pipeline
        self.params_list = GridSearch._expand_params(params_grid)
        self.results: pd.DataFrame = None
        self.best_score: float = None
        self.best_params: Dict = None

    def _expand_params(params_grid: Dict) -> List[Dict]:
        """
        Expands a grid of parameters into a list of all possible combinations.
        """
        values_list = [v for params in params_grid.values()
                       for v in params.values()]
        keys_list = [(step, param) for step, params_dict in params_grid.items()
                     for param in params_dict.keys()]
        cartesian_product = list(itertools.product(*values_list))
        params_grid_list = []
        for tuple in cartesian_product:
            params = {}
            for i, value in enumerate(tuple):
                step, param = keys_list[i]
                if step not in params:
                    params[step] = {}
                params[step][param] = value
            params_grid_list.append(params)
        return params_grid_list

    def _update_best(self):
        if self.results is not None and not self.results.empty:
            best_row = self.results.loc[self.results['score'].idxmax()]
            self.best_score = best_row['score']
            best_params = {key: best_row[key]
                           for key in self.results.columns if "__" in key}
            nested_best_params = {step: {} for step in set(
                [key.split("__")[0] for key in best_params.keys()])}
            for key, value in best_params.items():
                step, param = key.split("__", 1)
                nested_best_params[step][param] = value
            self.best_params = nested_best_params

    def _hash_params(params: Dict) -> str:
        """
        Hashes a dictionary of parameters into a single string.
        """
        def serialize(obj):
            """JSON serializer for objects not serializable by default json code"""
            if callable(obj):
                return obj.__name__  # Use function name for hashing
            raise TypeError(
                f"Object of type {obj.__class__.__name__} is not JSON serializable")
        return hash(json.dumps(params, default=serialize, sort_keys=True))

    def _flatten_params_dict(params_dict: Dict) -> Dict:
        """
        Flattens a dictionary of parameters into a single dictionary with concatenated keys.        
        """
        def value_to_string(value):
            return value.__name__ if callable(value) else str(value)
        return {f"{step}__{param}": value_to_string(value)
                for step, params in params_dict.items()
                for param, value in params.items()}

    def run(self, df: pd.DataFrame, output_dir=None, verbose=False, styled=True):
        """
        Applies the grid search on a given DataFrame and optionally saves the results to CSV files.

        Args:
            df (pd.DataFrame): The DataFrame to apply the grid search on.
            output_dir (str, optional): The directory to save the result CSV files. If None, files are not saved.

        Returns:
            pd.DataFrame: A DataFrame containing the results of the grid search.
        """
        results = []
        n = len(self.params_list)
        for i, params in enumerate(self.params_list):
            # TODO: check for duplicate params because of steps overriding global params
            if verbose:
                print(f"Iteration {i+1} of {n}")
                print("Params: ", params)
            self.pipeline.update_params(params)
            df_result = self.pipeline.run(df.copy(), verbose)
            index = GridSearch._hash_params(params)
            if output_dir is not None:
                full_path = os.path.join(os.getcwd(), output_dir)
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                df_result.to_csv(f"{full_path}/{index}.csv")
            result = {
                **GridSearch._flatten_params_dict(params),
                'score': self.pipeline.score,
                'lables': self.pipeline.labels,
                'Confusion_matrix': self.pipeline.cm,
                'input_cost': self.pipeline.statistics.input_cost,
                'output_cost': self.pipeline.statistics.output_cost,
                'total_latency': self.pipeline.statistics.total_latency,
                'input_tokens': self.pipeline.statistics.input_tokens,
                'output_tokens': self.pipeline.statistics.output_tokens,
                'num_success': self.pipeline.statistics.num_success,
                'num_failure': self.pipeline.statistics.num_failure,
                'index': index
            }
            if verbose:
                print("Result: ", result)
            results.append(result)
        self.results = pd.DataFrame(results)
        self._update_best()

        if styled:
            higher_columns = ['score']
            lower_columns = ['input_cost', 'output_cost', 'total_latency']
            return df_apply_gradients(self.results, higher_columns, lower_columns)
        return self.results
