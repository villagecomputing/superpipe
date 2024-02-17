import itertools
import json
import os
import pandas as pd
from .pipeline import Pipeline


class GridSearch:
    def __init__(self, pipeline: Pipeline, params_grid: dict):
        self.pipeline = pipeline
        self.params_list = GridSearch._expand_params(params_grid)
        self.results = None

    def _expand_params(params_grid):
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

    def _flatten_params_dict(params_dict):
        return {f"{step}__{param}": value for step, params in params_dict.items() for param, value in params.items()}

    def apply(self, df: pd.DataFrame, output_dir=None):
        results = []
        for i, params in enumerate(self.params_list):
            print(f"Iteration {i+1} of {len(self.params_list)}")
            print("Params: ", params)
            self.pipeline.update_params(params)
            df_result = self.pipeline.apply(df.copy())
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
                'num_success': self.pipeline.statistics.num_success,
                'num_failure': self.pipeline.statistics.num_failure,
                'total_latency': self.pipeline.statistics.total_latency,
                'index': index
            }
            print("Result: ", result)
            results.append(result)
        self.results = pd.DataFrame(results)
        return self.results
