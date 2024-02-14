from typing import Callable, Union, Dict
import pandas as pd
from pydantic import BaseModel
from labelkit.steps import Step, T
from labelkit.llm import get_structured_llm_response, StructuredLLMResponse
from labelkit.pydantic import describe_pydantic_model


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


class LLMStep(Step):
    def __init__(
            self,
            out_model: T,
            model: str,
            prompt: Callable[[Union[pd.Series, Dict]], str],
            name: str = None):
        super().__init__(out_model, name, model=model, prompt=prompt)
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
        prompt = self.params.get('prompt')
        prompt_main = prompt(input)
        output_schema = describe_pydantic_model(self.out_model)
        return BASE_PROMPT.format(prompt_main=prompt_main, output_schema=output_schema)

    def prompt_llm(self, prompt):
        model = self.params.get('model')
        if not model:
            raise ValueError('Must set model param')
        return get_structured_llm_response(prompt, model)

    def apply(self, data: Union[pd.DataFrame, Dict]):
        name = self.name
        fields = self.out_model.model_fields.keys()

        def _apply(row):
            try:
                compiled_prompt = self.compile_structured_prompt(row)
                response = self.prompt_llm(compiled_prompt)
            except Exception as e:
                # TODO: need better error logging here include stacktrace
                response = StructuredLLMResponse(
                    success=False, error=str(e), latency=0)
            self._update_statistics(response)
            result = {f"__{name}__": response.model_dump()}
            if response.success:
                content = response.content
                for field in fields:
                    # TODO: handle missing fields instead of printing
                    if field not in content:
                        print(
                            f"Step {name}: Missing field {field} in response {content}")
                    val = content.get(field)
                    result[field] = val or ""
            return result

        if isinstance(data, pd.DataFrame):
            new_fields = data.apply(lambda x: pd.Series(_apply(x)), axis=1)
            data[new_fields.columns] = new_fields
        else:
            data.update(_apply(data))

        return data
