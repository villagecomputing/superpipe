import time
import json
from pydantic import BaseModel
from typing import Optional
from openai.types.chat.completion_create_params import CompletionCreateParamsNonStreaming
from superpipe.models import *
from superpipe.clients import get_client, openrouter_models


class LLMResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    success: bool = False
    error: Optional[str] = None
    latency: float = 0.0
    content: str = ""


class StructuredLLMResponse(LLMResponse):
    content: dict = {}


def get_llm_response(
        prompt: str,
        model: str = gpt35,
        args={}) -> LLMResponse:
    if model in openrouter_models:
        return get_llm_response_openrouter(prompt, model, args)
    if model in [claude3_haiku, claude3_sonnet, claude3_opus]:
        return get_llm_response_anthropic(prompt, model, args)
    return get_llm_response_openai(prompt, model, args)


def get_llm_response_openrouter(
        prompt: str,
        model: str = "openrouter/auto",
        args={},
        system: str = None,) -> LLMResponse:
    response = LLMResponse()
    res = None
    client = get_client(model)
    if client is None:
        raise ValueError("Unsupported model: ", model)
    try:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        start_time = time.perf_counter()
        res = client.chat.completions.create(
            model=model,
            messages=messages,
            **args
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


def get_structured_llm_response_openrouter(
        prompt: str,
        model: str = "openrouter/auto",
        args={},
        system: str = None,) -> LLMResponse:
    return get_llm_response_openrouter(prompt, model, system, args)


def get_llm_response_anthropic(
        prompt: str,
        model: str = claude3_haiku,
        args={}) -> LLMResponse:
    response = LLMResponse()
    res = None
    client = get_client(model)
    if client is None:
        raise ValueError(f"""Unsupported model: {model}. Currently Superpipe only supports OpenAI, Anthropic and OpenRouter models.
                         If you're trying to use a supported model, you might be missing the appropriate api key.""")
    try:
        start_time = time.perf_counter()
        res = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            **args
        )
        end_time = time.perf_counter()
        response.latency = end_time - start_time
        response.input_tokens = res.usage.input_tokens
        response.output_tokens = res.usage.output_tokens
        response.input_cost, response.output_cost = get_cost(
            response.input_tokens, response.output_tokens, model)
        response.content = res.content[0].text
        response.success = True
    except Exception as e:
        response.success = False
        response.error = str(e)
    return response


def get_llm_response_openai(
        prompt: str,
        model=gpt35,
        args: CompletionCreateParamsNonStreaming = {},
        system: str = None,) -> LLMResponse:
    response = LLMResponse()
    res = None
    client = get_client(model)
    if client is None:
        raise ValueError("Unsupported model: ", model)
    try:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        start_time = time.perf_counter()
        res = client.chat.completions.create(
            model=model,
            messages=messages,
            **args
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


def get_structured_llm_response(
        prompt: str,
        model: str = gpt35,
        args={}) -> StructuredLLMResponse:
    if model in [claude3_haiku, claude3_sonnet, claude3_opus]:
        return get_structured_llm_response_anthropic(prompt, model, args)
    return get_structured_llm_response_openai(prompt, model, args)


def get_structured_llm_response_openrouter(
        prompt: str,
        model: str = "openrouter/auto",
        args={}) -> StructuredLLMResponse:
    print("Warning: Not all OpenRouter models support structured output, this may cause unexpected issues.")
    system = "You are a helpful assistant designed to output JSON."
    updated_args = {**args, "response_format": {"type": "json_object"}}
    response = get_llm_response_openrouter(prompt, model, updated_args, system)
    return StructuredLLMResponse(
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        input_cost=response.input_cost,
        output_cost=response.output_cost,
        success=response.success,
        error=response.error,
        latency=response.latency,
        content=json.loads(response.content) if response.success else {},
    )


def get_structured_llm_response_anthropic(
        prompt: str,
        model: str = claude3_haiku,
        args={}) -> StructuredLLMResponse:
    print("Warning: Anthropic models do not support structured output, this may cause unexpected issues.")
    updated_args = {
        **args,
        "system": "You are a helpful assistant designed to output JSON. Return only JSON, nothing else."
    }
    return get_llm_response_anthropic(
        prompt,
        model,
        args=updated_args)


def get_structured_llm_response_openai(
        prompt: str,
        model=gpt35,
        args: CompletionCreateParamsNonStreaming = {}) -> StructuredLLMResponse:
    system = "You are a helpful assistant designed to output JSON."
    updated_args = {**args, "response_format": {"type": "json_object"}}

    response = get_llm_response_openai(prompt, model, updated_args, system)
    if response.error:  # models before 1163 do not support response_format param
        response = get_llm_response_openai(prompt, model, args, system)

    return StructuredLLMResponse(
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        input_cost=response.input_cost,
        output_cost=response.output_cost,
        success=response.success,
        error=response.error,
        latency=response.latency,
        content=json.loads(response.content) if response.success else {},
    )
