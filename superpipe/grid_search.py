import itertools
import json
import os
import pandas as pd
from typing import Dict, List
from superpipe.pipeline import Pipeline


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

    def _flatten_params_dict(params_dict: Dict) -> Dict:
        """
        Flattens a dictionary of parameters into a single dictionary with concatenated keys.        
        """
        return {f"{step}__{param}": value for step, params in params_dict.items() for param, value in params.items()}

    def apply(self, df: pd.DataFrame, output_dir=None, verbose=False):
        """
        Applies the grid search on a given DataFrame and optionally saves the results to CSV files.

        Args:
            df (pd.DataFrame): The DataFrame to apply the grid search on.
            output_dir (str, optional): The directory to save the result CSV files. If None, files are not saved.

        Returns:
            pd.DataFrame: A DataFrame containing the results of the grid search.
        """
        results = []
        for i, params in enumerate(self.params_list):
            # TODO: check for duplicate params because of steps overriding global params
            print(f"Iteration {i+1} of {len(self.params_list)}")
            print("Params: ", params)
            self.pipeline.update_params(params)
            df_result = self.pipeline.apply(df.copy(), verbose)
            index = hash(json.dumps(params, sort_keys=True))
            if output_dir is not None:
                full_path = os.path.join(os.getcwd(), output_dir)
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                df_result.to_csv(f"{full_path}/{index}.csv")
            result = {
                **GridSearch._flatten_params_dict(params),
                'score': self.pipeline.score,
                'input_tokens': self.pipeline.statistics.input_tokens,
                'output_tokens': self.pipeline.statistics.output_tokens,
                'input_cost': self.pipeline.statistics.input_cost,
                'output_cost': self.pipeline.statistics.output_cost,
                'num_success': self.pipeline.statistics.num_success,
                'num_failure': self.pipeline.statistics.num_failure,
                'total_latency': self.pipeline.statistics.total_latency,
                'index': index
            }
            print("Result: ", result)
            results.append(result)
        self.results = pd.DataFrame(results)
        self._update_best()
        return self.results
