from openai import OpenAI
from labelkit.models import *

# TODO: add support for non-openai providers

openai_client = None
client_for_model = {}


def init_openai(api_key=None, base_url=None):
    global openai_client
    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    client_for_model[gpt35] = openai_client
    client_for_model[gpt4] = openai_client
    get_model_pricing()

def get_client(model):
    if openai_client is None:
        init_openai()
    return client_for_model.get(model)


def set_client_for_model(model, api_key, base_url):
    client_for_model[model] = OpenAI(api_key=api_key, base_url=base_url)

input_cost_per_1000_tokens = {}
output_cost_per_1000_tokens = {}

def get_model_pricing():
    global input_cost_per_1000_tokens, output_cost_per_1000_tokens
    if not input_cost_per_1000_tokens or not output_cost_per_1000_tokens:
        # Instead of fetching, directly use the model_pricing dictionary
        for model_id, pricing in model_pricing.items():
            input_cost_per_1000_tokens[model_id] = pricing['input_cost_per_1000']
            output_cost_per_1000_tokens[model_id] = pricing['output_cost_per_1000']
    return input_cost_per_1000_tokens, output_cost_per_1000_tokens
