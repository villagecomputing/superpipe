from typing import Callable, Union, Dict, TypeVar, Generic
import pandas as pd
from pydantic import BaseModel
from superpipe.steps.step import Step
from superpipe.llm import get_llm_response, LLMResponse


class LLMStepStatistics(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0


class LLMStep(Step):
    """
    A step in a pipeline that utilizes a Language Model (LLM) to process data.

    This step compiles a prompt from the input data, sends it to the LLM, and receives a response string.

    Attributes:
        model (str): The identifier of the LLM to be used.
        prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes input data and returns a prompt string.
        name (str, optional): The name of the step. Defaults to None.
        statistics (LLMStepStatistics): Statistics about the LLM calls made by this step.
    """

    def __init__(
            self,
            model: str,
            prompt: Callable[[Union[Dict, pd.Series]], str],
            name: str = None):
        """
        Initializes a new instance of the LLMStep class.

        Args:
            model (str): The identifier of the LLM to be used.
            prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes input data and returns a prompt string.
            name (str, optional): The name of the step. Defaults to None.
        """
        super().__init__(name)
        self.model = model
        self.prompt = prompt
        self.statistics = LLMStepStatistics()

    def update_params(self, params: Dict):
        """
        Updates the parameters of the step.
        Also resets the statistics to ensure they reflect the performance after the parameter update.

        Args:
            params (Dict): A dictionary of parameters to update.
        """
        super().update_params(params)
        self.statistics = LLMStepStatistics()

    def _update_statistics(self, response: LLMResponse):
        """
        Updates the statistics based on the response from the LLM.

        Args:
            response (LLMResponse): The response from the LLM.
        """
        self.statistics.input_tokens += response.input_tokens
        self.statistics.output_tokens += response.output_tokens
        self.statistics.total_latency += response.latency
        if response.success:
            self.statistics.num_success += 1
        else:
            self.statistics.num_failure += 1

    def _run(self, row: Union[pd.Series, Dict]) -> Dict:
        """
        Applies the LLM step to a single row of data.

        This method compiles the prompt, sends it to the LLM, and processes the response.

        Args:
            row (Union[pd.Series, Dict]): The input data row.

        Returns:
            Dict: The processed data, including the LLM's response
        """
        model = self.model
        try:
            compiled_prompt = self.prompt(row)
            response = get_llm_response(compiled_prompt, model)
        except Exception as e:
            # TODO: need better error logging here include stacktrace
            response = LLMResponse(
                success=False, error=str(e), latency=0)
        self._update_statistics(response)
        result = {f"__{self.name}__": response.model_dump()}
        # TODO: how should we handle failure cases?
        if response.success:
            result[f"{self.name}"] = response.content
        return result
