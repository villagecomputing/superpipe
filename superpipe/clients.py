import os
from openai import OpenAI
from anthropic import Anthropic
from superpipe.models import *

# TODO: add support for non-openai providers

client_for_model = {}


def init_openai(api_key=None, base_url=None):
    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    client_for_model[gpt35] = openai_client
    client_for_model[gpt4] = openai_client


def init_anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")):
    anthropic_client = Anthropic(api_key=api_key)
    client_for_model[claude3_haiku] = anthropic_client
    client_for_model[claude3_sonnet] = anthropic_client
    client_for_model[claude3_opus] = anthropic_client


def get_client(model):
    if client_for_model.get(gpt35) is None or \
            client_for_model.get(gpt4) is None:
        init_openai()
    if client_for_model.get(claude3_haiku) is None or \
            client_for_model.get(claude3_sonnet) is None or \
            client_for_model.get(claude3_opus) is None:
        init_anthropic()
    return client_for_model.get(model)


def set_client_for_model(model, api_key, base_url, pricing=None):
    client_for_model[model] = OpenAI(api_key=api_key, base_url=base_url)
    if pricing is not None:
        update_pricing({model: pricing})
