import pickle
import hashlib
from typing import List, Callable, Union, Dict, Optional
from collections import defaultdict
from dataclasses import dataclass, field
import pandas as pd
from prettytable import PrettyTable
from superpipe.steps import Step, LLMStep, LLMStructuredStep, LLMStructuredCompositeStep
from superpipe.config import is_dev, studio_enabled


@dataclass
class PipelineStatistics:
    score: Optional[float] = None
    input_tokens: dict = field(default_factory=lambda: defaultdict(int))
    output_tokens: dict = field(default_factory=lambda: defaultdict(int))
    input_cost: float = 0.0
    output_cost: float = 0.0
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0

    def __str__(self):
        table = PrettyTable()
        table.header = False
        if self.score is not None:
            table.add_row(["score", str(self.score)], divider=True)
        table.add_row(["input_tokens", str(
            dict(self.input_tokens))], divider=True)
        table.add_row(["output_tokens", str(
            dict(self.output_tokens))], divider=True)
        table.add_row(["input_cost", f"${self.input_cost}"], divider=True)
        table.add_row(
            ["output_cost", f"${self.output_cost}"], divider=True)
        table.add_row(["num_success", str(self.num_success)], divider=True)
        table.add_row(["num_failure", str(self.num_failure)], divider=True)
        table.add_row(["total_latency", str(self.total_latency)])
        return table.get_string()


class Pipeline:
    """
    A class representing a pipeline of steps to process data.

    Attributes:
        steps (List[Step]): A list of steps (processing units) in the pipeline.
        evaluation_fn (Callable[[any], bool], optional): An optional function to evaluate the processed data.
        data (Union[pd.DataFrame, Dict], optional): The data processed by the pipeline. Initially None.
        score (float, optional): The evaluation score of the processed data. Initially None.
        statistics (PipelineStatistics): Statistics of the pipeline's execution.

    Methods:
        run(data): Applies the pipeline steps to the input data.
        update_params(params): Updates the parameters of the pipeline steps.
        evaluate(evaluation_fn=None): Evaluates the processed data using an evaluation function.
        _aggregate_statistics(data): Aggregates statistics from the pipeline steps.
    """

    def __init__(self,
                 steps: List[Step],
                 evaluation_fn: Callable[[any], Union[bool, float]] = None,
                 output_fields: List[str] = None,
                 name: str = None):
        if len(steps) == 0:
            raise ValueError("Pipeline must contain at least one step")
        self.steps = steps
        self.evaluation_fn = evaluation_fn
        self.output_fields = output_fields or steps[-1].output_fields()
        self.data = None
        self.score = None
        self.name = name or self.__class__.__name__
        self.statistics = PipelineStatistics()

    def run_experiment(self, data, verbose=True, description=None):
        def run_steps(row: pd.Series):
            for step in self.steps:
                step.run(row, verbose)
            return row

        if studio_enabled():
            from studio import run_pipeline_with_experiment, Dataset, create_experiment
            if isinstance(data, pd.DataFrame):
                dataset = Dataset(data=data, name=f"{self.name}_dataset")
                print(f"Created dataset {dataset.id}")
            elif isinstance(data, str):
                dataset = Dataset(id=data)
            elif isinstance(data, Dataset):
                pass
            experiment_id = create_experiment(
                dataset_id=dataset.id,
                name=self.name,
                parameters=self.get_params(),
                group_id=self.fingerprint(),
                description=description)
            print(f"Created experiment {experiment_id}")
            run_steps = run_pipeline_with_experiment(
                experiment_id, run_steps, self)
            df = dataset.data
            if verbose and is_dev:
                from tqdm import tqdm
                tqdm.pandas(desc=f"Running pipeline row-wise")
                results = df.progress_apply(run_steps, axis=1)
            else:
                results = df.apply(run_steps, axis=1)
            df[results.columns] = results
            self.data = df
            if self.evaluation_fn is not None:
                self.evaluate()
            self._aggregate_statistics(df)
            return df
        else:
            raise ValueError(
                "Superpipe Studio must be enabled to run experiments")

    def run(self,
            data: Union[pd.DataFrame, Dict],
            enable_logging=False,
            row_wise=True,
            verbose=True):
        def run_steps(row):
            for step in self.steps:
                step.run(row, verbose)
            return row

        # Note: currently running row-wise is ~40% slower than step-wise (because of memory overhead?)
        if row_wise:
            if enable_logging and studio_enabled():
                from studio import run_pipeline_with_log
                run_steps = run_pipeline_with_log(run_steps, self)
            if isinstance(data, pd.DataFrame):
                if verbose and is_dev:
                    from tqdm import tqdm
                    tqdm.pandas(desc=f"Running pipeline row-wise")
                    results = data.progress_apply(run_steps, axis=1)
                else:
                    results = data.apply(run_steps, axis=1)
                data[results.columns] = results
            else:
                run_steps(data)
        else:
            # logging not supported for step-wise execution
            for step in self.steps:
                step.run(data, verbose)
        if isinstance(data, pd.DataFrame):
            self.data = data
            if self.evaluation_fn is not None:
                self.evaluate()
        self._aggregate_statistics(data)
        return data

    def fingerprint(self, deep=False):
        fingerprint_obj = {
            "name": self.name,
            "steps": [step.fingerprint(deep) for step in self.steps]
        }
        object_bytes = pickle.dumps(fingerprint_obj)
        hash_object = hashlib.sha256()
        hash_object.update(object_bytes)
        return hash_object.hexdigest()

    def get_params(self):
        return {
            k: v for k, v in [
                (step.name, step.get_params()) for step in self.steps
            ]
        }

    # TODO: only include params relevant for each step, raise if param is not found in any step
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
        self.data[f"__{evaluation_fn.__name__}__"] = results
        self.score = results.sum() / len(results)
        return self.score

    def _aggregate_statistics(self, data: Union[pd.DataFrame, Dict]):
        self.statistics = PipelineStatistics()
        if self.score is not None:
            self.statistics.score = self.score
        if isinstance(data, pd.DataFrame):
            success = data.apply(lambda x: True, axis=1)
        else:
            success = True
        for step in self.steps:
            self.statistics.input_cost += step.statistics.input_cost
            self.statistics.output_cost += step.statistics.output_cost
            self.statistics.total_latency += step.statistics.total_latency
            # TODO: this needs to work for CustomSteps that make LLM calls too
            if isinstance(step, LLMStep) or isinstance(step, LLMStructuredStep) \
                    or isinstance(step, LLMStructuredCompositeStep):
                model = step.model
                # TODO: this assumed that each step has a unique model which is not true for composite step
                self.statistics.input_tokens[model] += step.statistics.input_tokens
                self.statistics.output_tokens[model] += step.statistics.output_tokens

                # TODO: success calculation needs to work for non LLM steps too
                if isinstance(data, pd.DataFrame):
                    success = success & data.apply(
                        lambda x: x[f"__{step.name}__"]["success"], axis=1)
                    self.statistics.num_success = success.sum()
                    self.statistics.num_failure = len(
                        data) - self.statistics.num_success
                else:
                    success = success & data[f"__{step.name}__"]["success"]
                    self.statistics.num_success = 1 if success else 0
