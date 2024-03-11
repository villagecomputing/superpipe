import time
import json
from pydantic import BaseModel
from superpipe.models import gpt35, get_cost
from superpipe.openai import get_client


class StructuredLLMResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    success: bool = False
    error: str = None
    latency: float = 0.0
    content: dict = {}


class LLMResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    success: bool = False
    error: str = None
    latency: float = 0.0
    content: str = ""


def get_llm_response(prompt: str, model=gpt35) -> LLMResponse:
    response = LLMResponse()
    res = None
    client = get_client(model)
    if client is None:
        raise ValueError("Unsupported model: ", model)
    try:
        start_time = time.perf_counter()
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        end_time = time.perf_counter()
        response.latency = end_time - start_time
        response.input_tokens = res.usage.prompt_tokens
        response.output_tokens = res.usage.completion_tokens
        response.input_cost, response.output_cost = get_cost(
            response.input_tokens, response.output_tokens, model)
        response.content = res.choices[0].message.content
        response.success = True
    except Exception as e:
        response.success = False
        response.error = str(e)
    return response


def get_structured_llm_response(prompt: str, model=gpt35) -> StructuredLLMResponse:
    """
    Sends a prompt to a specified language model and returns a structured response.

    The desired output schema should be described within the prompt.

    This function sends a prompt to a language model, specified by the `model` parameter,
    and structures the response into a `StructuredLLMResponse` object. It handles errors
    gracefully, populating the error attribute of the response object if necessary.

    Also measures the latency of the request and populates the latency attribute of the response object.

    Args:
        prompt (str): The input prompt to send to the language model.
        model: The language model to use. Defaults to `gpt35`.

    Returns:
        StructuredLLMResponse: An object containing structured information about the
        response from the language model, including input and output tokens, success
        status, error message (if any), latency, and the content of the response.

    Raises:
        ValueError: If the specified model is not supported.
    """

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
        response.input_cost, response.output_cost = get_cost(
            response.input_tokens, response.output_tokens, model)
        response.content = json.loads(res.choices[0].message.content)
        response.success = True
    except Exception as e:
        response.success = False
        if res is None:
            response.error = str(e)
        else:
            response.error = f"Failed to parse json: ${res.choices[0].message.content}"
    return response
