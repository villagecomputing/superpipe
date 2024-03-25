from typing import Callable, Union, Dict, TypeVar, Generic
import pandas as pd
from pydantic import BaseModel
from openai.types.chat.completion_create_params import CompletionCreateParamsNonStreaming
from superpipe.llm import (
    get_structured_llm_response,
    StructuredLLMResponse,
    get_llm_response)
from superpipe.pydantic import describe_pydantic_model
from superpipe.steps.llm_step import LLMStep, StepResult
from superpipe.steps.utils import combine_step_row_statistics
from superpipe.models import gpt35

T = TypeVar('T', bound=BaseModel)


BASE_PROMPT = """
{prompt_main}

Return your response in the format given below as a Pydantic model schema:
{output_schema}
"""


class LLMStructuredCompositeStep(LLMStep, Generic[T]):
    def __init__(
            self,
            model: str,
            prompt: Callable[[Union[Dict, pd.Series]], str],
            out_schema: T,
            structured_model: str = gpt35,
            openai_args: CompletionCreateParamsNonStreaming = {},
            name: str = None):
        """
        A pipeline step that uses a structured and an unstructured language model to process data.
        Use this step when the model or provider does not support JSON mode natively.

        Attributes:
            model (str): Identifier for the unstructured LLM.
            prompt (Callable[[Union[Dict, pd.Series]], str]): Function generating the prompt from input data.
            out_schema (T): Pydantic model defining the expected structured output.
            structured_model (str): Identifier for the structured LLM. Defaults to gpt35.
            name (str, optional): Name of the step.
        """
        super().__init__(model, prompt, openai_args, name)
        self.structured_model = structured_model
        self.out_schema = out_schema

    def _compile_structured_prompt(self, unstructured: str):
        prompt_main = f"""
        You are a helpful assistant designed to output JSON. Turn the following unstructured data into a structured JSON object.
        
        {unstructured}
        """
        output_schema = describe_pydantic_model(self.out_schema)
        return BASE_PROMPT.format(prompt_main=prompt_main, output_schema=output_schema)

    def _run(self, row: Union[pd.Series, Dict]) -> Dict:
        """
        Processes a single row of data. Does one LLM call to generate an unstructured response and another to structure it.

        Args:
            row (Union[pd.Series, Dict]): The input data row.

        Returns:
            StepResult: The processed data and statistics about the LLM calls.
        """
        model = self.model
        prompt = self.prompt
        structured_model = self.structured_model
        openai_args = self.openai_args
        fields = self.out_schema.model_fields.keys()
        compiled_prompt = prompt(row)
        try:
            response = get_llm_response(compiled_prompt, model, openai_args)
            statistics_first = self._get_row_statistics(response)
            if response.success:
                compiled_prompt = self._compile_structured_prompt(
                    response.content)
                response = get_structured_llm_response(
                    compiled_prompt, structured_model, openai_args)
            else:
                response = StructuredLLMResponse(
                    success=False, error=response.error, latency=0)
        except Exception as e:
            # TODO: need better error logging here include stacktrace
            response = StructuredLLMResponse(
                success=False, error=str(e), latency=0)
        # TODO: combine model dumps of both LLM calls
        result = {f"__{self.name}__": response.model_dump()}
        statistics_second = self._get_row_statistics(response)
        statistics = combine_step_row_statistics(
            [statistics_first, statistics_second])
        # TODO: how should we handle failure cases
        if response.success:
            content = response.content
            for field in fields:
                # TODO: handle missing fields instead of printing
                if field not in content:
                    print(
                        f"Step {self.name}: Missing field {field} in response {content}")
                val = content.get(field)
                result[field] = val if val is not None else ""
        return StepResult(fields=result, statistics=statistics)
