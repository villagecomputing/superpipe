import requests
import os
from openai import OpenAI
from anthropic import Anthropic
from superpipe.models import *

# TODO: add support for non-openai providers

client_for_model = {}
openrouter_models = []


def init_openai(api_key, base_url=None):
    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    client_for_model[gpt35] = openai_client
    client_for_model[gpt4] = openai_client


def init_anthropic(api_key):
    anthropic_client = Anthropic(api_key=api_key)
    client_for_model[claude3_haiku] = anthropic_client
    client_for_model[claude3_sonnet] = anthropic_client
    client_for_model[claude3_opus] = anthropic_client


def init_openrouter(api_key):
    base_url = "https://openrouter.ai/api/v1"
    openrouter_client = OpenAI(api_key=api_key, base_url=base_url)
    models_json = requests.get(f"{base_url}/models").json()
    openrouter_models.extend([model['id'] for model in models_json['data']])
    pricing_list = [(model['pricing']['prompt'], model['pricing']
                     ['completion']) for model in models_json['data']]
    pricing_list = [(float(p[0])*1e6, float(p[1])*1e6) if float(p[0]) > 0 else (0, 0)
                    for p in pricing_list]
    for i, model in enumerate(openrouter_models):
        client_for_model[model] = openrouter_client
        set_pricing({model: pricing_list[i]})


def get_client(model):
    if client_for_model.get("openrouter/auto") is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key is not None:
            init_openrouter(api_key)
    if client_for_model.get(gpt35) is None or \
            client_for_model.get(gpt4) is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is not None:
            init_openai(api_key)
    if client_for_model.get(claude3_haiku) is None or \
            client_for_model.get(claude3_sonnet) is None or \
            client_for_model.get(claude3_opus) is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key is not None:
            init_anthropic(api_key)
    return client_for_model.get(model)


def set_client_for_model(model, api_key, base_url, pricing=None):
    client_for_model[model] = OpenAI(api_key=api_key, base_url=base_url)
    if pricing is not None:
        set_pricing({model: pricing})
