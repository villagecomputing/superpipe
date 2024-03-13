# Models

Superpipe conveniently comes with pricing and shorthand for some commonly used models.

```
gpt4 = "gpt-4-turbo-preview"
gpt35 = "gpt-3.5-turbo-0125"
mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"
mistral = "mistralai/Mistral-7B-Instruct-v0.1"
codellama = "togethercomputer/CodeLlama-34b-Instruct"
llama270b = "meta-llama/Llama-2-70b-chat-hf"
stripedhyena = "togethercomputer/StripedHyena-Nous-7B"
```

## Setting or changing the model provider
You can use any model and model provider with Superpipe as long as it conforms to the OpenAI spec. 

For example, Together, Anyscale, and OpenRouter all provide Superpipe compatible endpoints for open source models. 

For non OpenAI you need to provide a `baseURL` when using the model. You can do this by calling the `set_client_for_model` function.

`set_client_for_model(model_name, api_key, base_url, pricing)`

The `pricing` dictionary takes a model name as the key and a tuple for the input and output price per million tokens as values.

```python
openai.set_client_for_model(
    model_name='google/gemma-7b-it:free', 
    api_key="OPEN_ROUTER_API_KEY", 
    base_url="https://openrouter.ai/api/v1", 
    pricing={
        'google/gemma-7b-it:free': (0, 0)
    }
)
```
