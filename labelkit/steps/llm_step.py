from typing import TypedDict, Callable, Union, Dict, TypeVar, Generic
import pandas as pd
from pydantic import BaseModel
from labelkit.steps import Step
from labelkit.llm import get_structured_llm_response, StructuredLLMResponse
from labelkit.pydantic import describe_pydantic_model
from labelkit.util import validate_dict

T = TypeVar('T', bound=BaseModel)


class LLMStepStatistics(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    num_success: int = 0
    num_failure: int = 0
    total_latency: float = 0.0


BASE_PROMPT = """
{prompt_main}

Return your response in the format given below as a Pydantic model schema:
{output_schema}
"""


class LLMStepParams(TypedDict):
    model: str
    prompt: Callable[[Union[Dict, pd.Series]], str]


class LLMStep(Step, Generic[T]):
    def __init__(
            self,
            params: LLMStepParams,
            out_model: T,
            name: str = None):
        super().__init__(name)
        validate_dict(params, LLMStepParams)
        self.params = params
        self.out_model = out_model
        self.statistics = LLMStepStatistics()

    def update_params(self, params):
        super().update_params(params)
        self.statistics = LLMStepStatistics()

    def _update_statistics(self, response: StructuredLLMResponse):
        self.statistics.input_tokens += response.input_tokens
        self.statistics.output_tokens += response.output_tokens
        self.statistics.total_latency += response.latency
        if response.success:
            self.statistics.num_success += 1
        else:
            self.statistics.num_failure += 1

    def compile_structured_prompt(self, input: dict):
        prompt = self.params['prompt']
        prompt_main = prompt(input)
        output_schema = describe_pydantic_model(self.out_model)
        return BASE_PROMPT.format(prompt_main=prompt_main, output_schema=output_schema)

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        model = self.params['model']
        fields = self.out_model.model_fields.keys()
        try:
            compiled_prompt = self.compile_structured_prompt(row)
            response = get_structured_llm_response(compiled_prompt, model)
        except Exception as e:
            # TODO: need better error logging here include stacktrace
            response = StructuredLLMResponse(
                success=False, error=str(e), latency=0)
        self._update_statistics(response)
        result = {f"__{self.name}__": response.model_dump()}
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
