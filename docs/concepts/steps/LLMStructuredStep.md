# Structured LLM Step

The `LLMStructuredStep` is used to create structured responses.

An `LLMStructuredStep` instance takes a Pydantic model and a prompt generator function as arguments. The pydantic model specifies the output structure. The prompt generator function defines how to generate a prompt from the input data. You can optionally provide a model and step name. 

## Statistics
`LLMStructuredStep` returns useful statistics about the LLM call for each row.  


| Stat name       | Description |
|-------------|----------|
|input_tokens | Number of input tokens used.
|output_tokens | Number of output tokens used.
|input_cost| Input cost of running the LLM call.
|output_cost | Output cost of running the LLM call.
|num_success | Number of succesful calls.
|num_failure | Number of unsuccesful calls.
|total_latency | Latency for the LLM call.

## Example
In this example, we provide information about a business and three potential codes to choose from and we expect two structured fields in return, `reasoning` and `code`.

```python
from pydantic import BaseModel, Field

def business_code_prompt(row): return f"""
    You are given a business name and a list of google search results about a company.
    You are given 3 possible NAICS codes it could be -- pick the best one and explain your reasoning.

    Company name: {row['name']}
    NAICS options: {row['top3_codes']}
    Search results:
    {row['serp']}
"""


class BusinessCode(BaseModel):
    reasoning: str = Field(description="The thought process for why this is the best NAICS code")
    code: str = Field(description="The best NAICS code")

business_code_step = steps.LLMStructuredStep(
  model=models.gpt4,
  prompt=business_code_prompt,
  out_schema=BusinessCode,
  name="business_code")
```

## Supported models
`LLMStructuredStep` currently only works with models that support JSON mode. There may be other models not on this list that also work.

| model       | provider |
|-------------|----------|
| gpt4        | OpenAI   |
| gpt35       | OpenAI   |
| mixtral     | Together, Anyscale |
| mistral     | Together, Anyscale |
| codellama    | Together |

See the [models](../models.md) page for information on the mapping of model names to models.