import time
import json
from pydantic import BaseModel
from labelkit.models import gpt35
from labelkit.openai import get_client


class StructuredLLMResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    success: bool = False
    error: str = None
    latency: float = 0.0
    content: dict = {}


def get_structured_llm_response(prompt: str, model=gpt35) -> StructuredLLMResponse:
    response = StructuredLLMResponse()
    res = None
    client = get_client(model)
    if client is None:
        raise ValueError("Unsupported model: ", model)
    try:
        start_time = time.perf_counter()
        res = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        end_time = time.perf_counter()
        response.latency = end_time - start_time
        response.input_tokens = res.usage.prompt_tokens
        response.output_tokens = res.usage.completion_tokens
        response.content = json.loads(res.choices[0].message.content)
        response.success = True
    except Exception as e:
        response.success = False
        if res is None:
            response.error = str(e)
        else:
            response.error = f"Failed to parse json: ${res.choices[0].message.content}"
    return response
