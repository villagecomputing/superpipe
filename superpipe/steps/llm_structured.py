from typing import Callable, Union, Dict, TypeVar, Generic
import pandas as pd
from pydantic import BaseModel
from openai.types.chat.completion_create_params import CompletionCreateParamsNonStreaming
from superpipe.llm import get_structured_llm_response, StructuredLLMResponse
from superpipe.pydantic import describe_pydantic_model
from superpipe.steps.llm_step import LLMStep, StepResult

T = TypeVar('T', bound=BaseModel)


BASE_PROMPT = """
{prompt_main}

Return your response in the format given below as a Pydantic model schema:
{output_schema}
"""


class LLMStructuredStep(LLMStep, Generic[T]):
    """
    A step in a pipeline that utilizes a Language Model (LLM) to process data.

    This step compiles a structured prompt from the input data, sends it to the LLM,
    and processes the response according to a specified output schema.

    Attributes:
        model (str): The identifier of the LLM to be used.
        prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes input data and returns a prompt string.
        out_schema (T): The Pydantic model that defines the expected structure of the LLM's response.
        name (str, optional): The name of the step. Defaults to None.
        statistics (LLMStepStatistics): Statistics about the LLM calls made by this step.
    """

    def __init__(
            self,
            model: str,
            prompt: Callable[[Union[Dict, pd.Series]], str],
            out_schema: T,
            openai_args: CompletionCreateParamsNonStreaming = {},
            name: str = None):
        """
        Initializes a new instance of the LLMStructuredStep class.

        Args:
            model (str): The identifier of the LLM to be used.
            prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes input data and returns a prompt string.
            out_schema (T): The Pydantic model that defines the expected structure of the LLM's response.
            name (str, optional): The name of the step. Defaults to None.
        """
        super().__init__(model, prompt, openai_args, name)
        self.out_schema = out_schema

    def _compile_structured_prompt(self, input: dict):
        """
        Compiles a structured prompt from the input data.

        Args:
            input (dict): The input data for the prompt.

        Returns:
            str: The compiled prompt.
        """
        prompt = self.prompt
        prompt_main = prompt(input)
        output_schema = describe_pydantic_model(self.out_schema)
        return BASE_PROMPT.format(prompt_main=prompt_main, output_schema=output_schema)

    def _run(self, row: Union[pd.Series, Dict]) -> Dict:
        """
        Applies the LLM step to a single row of data.

        This method compiles the prompt, sends it to the LLM, and processes the response.

        Args:
            row (Union[pd.Series, Dict]): The input data row.

        Returns:
            Dict: The processed data, including the LLM's response and any extracted fields.
        """
        model = self.model
        fields = self.out_schema.model_fields.keys()
        compiled_prompt = self._compile_structured_prompt(row)
        openai_args = self.openai_args
        try:
            response = get_structured_llm_response(
                compiled_prompt, model, openai_args)
        except Exception as e:
            # TODO: need better error logging here include stacktrace
            response = StructuredLLMResponse(
                success=False, error=str(e), latency=0)
        result = {f"__{self.name}__": response.model_dump()}
        statistics = self._get_row_statistics(response)
        # TODO: how should we handle failure cases
        if response.success:
            content = response.content
            for field in fields:
                # TODO: handle missing fields instead of printing
                if field not in content:
                    print(
                        f"Step {self.name}: Missing field {field} in response {content}")
                val = content.get(field)
                result[field] = val or ""
        return StepResult(fields=result, statistics=statistics)
