from typing import Callable, Union, Dict
import pandas as pd
from superpipe.steps.step import Step, StepResult, StepRowStatistics
from superpipe.llm import get_llm_response, LLMResponse


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

    def _get_row_statistics(self, response: LLMResponse):
        """
        Create a StepRowStatistics object based on the response from the LLM.

        Args:
            response (LLMResponse): The response from the LLM.
        """
        return StepRowStatistics(
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            latency=response.latency,
            success=response.success,
            input_cost=response.input_cost,
            output_cost=response.output_cost
        )

    def _run(self, row: Union[pd.Series, Dict]) -> StepResult:
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
        result = {f"__{self.name}__": response.model_dump()}
        statistics = self._get_row_statistics(response)
        # TODO: how should we handle failure cases?
        if response.success:
            result[f"{self.name}"] = response.content
        return StepResult(fields=result, statistics=statistics)
