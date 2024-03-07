from typing import Callable, Union, Dict, TypeVar, Generic
import pandas as pd
from pydantic import BaseModel
from labelkit.steps import Step
from labelkit.llm import get_structured_llm_response, StructuredLLMResponse
from labelkit.pydantic import describe_pydantic_model

T = TypeVar('T', bound=BaseModel)


class LLMStepStatistics(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0
    input_cost: float = 0.0
    output_cost: float = 0.0


BASE_PROMPT = """
{prompt_main}

Return your response in the format given below as a Pydantic model schema:
{output_schema}
"""


class LLMStep(Step, Generic[T]):
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
            name: str = None):
        """
        Initializes a new instance of the LLMStep class.

        Args:
            model (str): The identifier of the LLM to be used.
            prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes input data and returns a prompt string.
            out_schema (T): The Pydantic model that defines the expected structure of the LLM's response.
            name (str, optional): The name of the step. Defaults to None.
        """
        super().__init__(name)
        self.model = model
        self.prompt = prompt
        self.out_schema = out_schema
        self.statistics = LLMStepStatistics()

    def update_params(self, params: Dict):
        """
        Updates the parameters of the step.

        This method resets the statistics to ensure they reflect the performance after the parameter update.

        Args:
            params (Dict): A dictionary of parameters to update.
        """
        super().update_params(params)
        self.statistics = LLMStepStatistics()

    def _update_statistics(self, response: StructuredLLMResponse):
        """
        Updates the statistics based on the response from the LLM.

        Args:
            response (StructuredLLMResponse): The response from the LLM.
        """
        self.statistics.input_tokens += response.input_tokens
        self.statistics.output_tokens += response.output_tokens
        self.statistics.total_latency += response.latency
        if response.success:
            self.statistics.num_success += 1
        else:
            self.statistics.num_failure += 1

        # Compute the cost
        self.statistics.input_cost += response.input_cost
        self.statistics.output_cost += response.output_cost

    def compile_structured_prompt(self, input: dict):
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

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
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
        try:
            compiled_prompt = self.compile_structured_prompt(row)
            response = get_structured_llm_response(compiled_prompt, model)
        except Exception as e:
            # TODO: need better error logging here include stacktrace
            response = StructuredLLMResponse(
                success=False, error=str(e), latency=0)
        self._update_statistics(response)
        result = {f"__{self.name}__": response.model_dump()}
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
        return result
