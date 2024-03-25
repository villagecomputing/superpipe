# Step 1: Build

_We'll use Superpipe to build a pipeline that receives a famous person's name and figures out their birthday, whether they're still alive, and if not, their cause of death._

This pipeline will work in 4 steps -

1. Do a google search with the person's name
2. Use an LLM to fetch the URL of their wikipedia page from the search results
3. Fetch the contents of the wikipedia page and convert them to markdown
4. Use an LLM to extract the birthdate and living or dead from the wikipedia contents

We'll build the pipeline, evaluate it on some data, and optimize it to maximize accuracy while reducing cost and latency.

[View notebook on Github](https://github.com/villagecomputing/superpipe/tree/main/docs/examples/web_scraping/web_scraping.ipynb)

```python
from superpipe.steps import LLMStructuredStep, CustomStep, SERPEnrichmentStep
from superpipe import models
from pydantic import BaseModel, Field

# Step 1: use Superpipe's built-in SERP enrichment step to search for the persons wikipedia page
# Include a unique "name" for the step that will used to reference this step's output in future steps

search_step = SERPEnrichmentStep(
  prompt= lambda row: f"{row['name']} wikipedia",
  name="search"
)

# Step 2: Use an LLM to extract the wikipedia URL from the search results
# First, define a Pydantic model that specifies the structured output we want from the LLM

class ParseSearchResult(BaseModel):
  wikipedia_url: str = Field(description="The URL of the Wikipedia page for the person")

# Then we use the built-in LLMStructuredStep and specify a model and a prompt
# The prompt is a function that has access to all the fields in the input as well as the outputs of previous steps

parse_search_step = LLMStructuredStep(
  model=models.gpt35,
  prompt= lambda row: f"Extract the Wikipedia URL for {row['name']} from the following search results: \n\n {row['search']}",
  out_schema=ParseSearchResult,
  name="parse_search"
)
```

Next, we'll create the final 2 steps of the pipeline and then the pipeline itself.

```python
from superpipe.pipeline import Pipeline
import requests
import html2text

h = html2text.HTML2Text()
h.ignore_links = True

# Step 3: we create a CustomStep that can execute any arbitrary function (transform)
# The function fetches the contents of the wikipedia url and converts them to markdown

fetch_wikipedia_step = CustomStep(
  transform=lambda row: h.handle(requests.get(row['wikipedia_url']).text),
  name="wikipedia"
)

# Step 4: we extract the date of birth, living/dead status and cause of death from the wikipedia contents

class ExtractedData(BaseModel):
    date_of_birth: str = Field(description="The date of birth of the person in the format YYYY-MM-DD")
    alive: bool = Field(description="Whether the person is still alive")
    cause_of_death: str = Field(description="The cause of death of the person. If the person is alive, return 'N/A'")

extract_step = LLMStructuredStep(
  model=models.gpt4,
  prompt= lambda row: f"""Extract the date of birth for {row['name']}, whether they're still alive \
  and if not, their cause of death from the following Wikipedia content: \n\n {row['wikipedia']}""",
  out_schema=ExtractedData,
  name="extract_data"
)

# Finally we define and run the pipeline

pipeline = Pipeline([
  search_step,
  parse_search_step,
  fetch_wikipedia_step,
  extract_step
])

pipeline.run({"name": "Jean-Paul Sartre"})
```

**Output**

When we run the pipeline, it returns an object that contains:

- the original input
- the outputs of each step in the pipeline
- some metadata associated with each LLM step

```json
{
  "name": "Jean-Paul Sartre",
  "search": "{\"searchParameters\":{\"q\":\"Jean-Paul Sartre wikipedia\",\"type\":\"search\",\"engine\":\"google\"},...}",
  "__parse_search__": {
    "input_tokens": 1704,
    "output_tokens": 23,
    "input_cost": 0.000852,
    "output_cost": 3.45e-5,
    "success": true,
    "error": null,
    "latency": 0.9851684169843793,
    "content": {
      "wikipedia_url": "https://en.wikipedia.org/wiki/Jean-Paul_Sartre"
    }
  },
  "wikipedia_url": "https://en.wikipedia.org/wiki/Jean-Paul_Sartre",
  "wikipedia": "Jump to content\n\nMain menu\n\nMain menu\n\nmove to sidebar hide\n\nNavigation\n\n  *...",
  "__extract_data__": {
    "input_tokens": 32542,
    "output_tokens": 35,
    "input_cost": 0.32542,
    "output_cost": 0.00105,
    "success": true,
    "error": null,
    "latency": 8.941851082723588,
    "content": {
      "date_of_birth": "1905-06-21",
      "alive": false,
      "cause_of_death": "pulmonary edema"
    }
  },
  "date_of_birth": "1905-06-21",
  "alive": false,
  "cause_of_death": "pulmonary edema"
}
```

Inspecting the last 3 fields of the output, we see that its results were correct.

Now, let's see how to [evaluate this pipeline](../evaluate) on a labeled dataset.

## Next Steps

[**Step 2: Evaluate**](../evaluate) &mdash; to learn about evaluating your pipelines.

[**Concepts**](../concepts) &mdash; to understand the core concepts behind Superpipe.

[**Examples**](../examples) &mdash; for more advanced examples and usage.
