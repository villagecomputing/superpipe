from typing import List, Callable, Union, Dict
from collections import defaultdict
from pydantic import BaseModel
import pandas as pd
from .steps import Step, LLMStep


class PipelineStatistics(BaseModel):
    input_tokens: dict = defaultdict(int)
    output_tokens: dict = defaultdict(int)
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0


class Pipeline:
    def __init__(self,
                 steps: List[Step],
                 evaluation_fn: Callable[[any], bool] = None):
        self.steps = steps
        self.evaluation_fn = evaluation_fn
        self.data = None
        self.score = None
        self.statistics = PipelineStatistics()

    def apply(self, data: Union[pd.DataFrame, Dict]):
        for step in self.steps:
            step.apply(data)
        self._aggregate_statistics(data)
        if isinstance(data, pd.DataFrame):
            self.data = data
            if self.evaluation_fn is not None:
                self.evaluate()
        return data

    def update_params(self, params: Dict):
        for step in self.steps:
            global_params = params.get('global', {})
            step_params = params.get(step.name, {})
            step.update_params({**global_params, **step_params})

    def evaluate(self, evaluation_fn=None):
        evaluation_fn = evaluation_fn or self.evaluation_fn
        if evaluation_fn is None:
            print("No evaluation function provided")
            return
        elif self.data is None:
            print("No data provided")
            return
        results = self.data.apply(lambda row: evaluation_fn(row), axis=1)
        self.score = results.sum() / len(results)
        return self.score

    def _aggregate_statistics(self, data: Union[pd.DataFrame, Dict]):
        self.statistics = PipelineStatistics()
        if isinstance(data, pd.DataFrame):
            success = data.apply(lambda x: True, axis=1)
        else:
            success = True
        for step in self.steps:
            if isinstance(step, LLMStep):
                model = step.params['model']
                self.statistics.input_tokens[model] += step.statistics.input_tokens
                self.statistics.output_tokens[model] += step.statistics.output_tokens
                self.statistics.total_latency += step.statistics.total_latency
                if isinstance(data, pd.DataFrame):
                    success = success & data.apply(
                        lambda x: x[f"__{step.name}__"]["success"], axis=1)
                    self.statistics.num_success = success.sum()
                    self.statistics.num_failure = len(
                        data) - self.statistics.num_success
                else:
                    success = success & data[f"__{step.name}__"]["success"]
                    self.statistics.num_success = 1 if success else 0
