# Step 3: Optimize

_In [Step 1](../build) we built a pipeline that receives a famous person's name and figures out their birthday, whether they're still alive, and if not, their cause of death. In [Step 2](../evaluate) we evaluated our pipeline on a dataset and found it was 100% accurate. Now we'll optimize it to reduce cost and speed while hopefully maintaining accuracy._

<hr>

First let's inspect the pipeline's statistics to figure out where there's room for improvement.

[View notebook on Github](https://github.com/villagecomputing/superpipe/tree/main/docs/examples/web_scraping/web_scraping.ipynb)

```python
for step in pipeline.steps:
  print(f"Step {step.name}:")
  print(f"- Latency: {step.statistics.total_latency}")
  print(f"- Cost: {step.statistics.input_cost + step.statistics.output_cost}")
```

```
Step search:
- Latency: 10.888118982315063
- Cost: 0.0
Step parse_search:
- Latency: 13.858203417155892
- Cost: 0.0085
Step wikipedia:
- Latency: 5.329825401306152
- Cost: 0.0
Step extract_data:
- Latency: 105.81304024951532
- Cost: 4.72056
```

Clearly the final step (`extract_data`) is the one responsible for the bulk of the cost and latency. This makes sense, because we're feeding in the entire wikipedia article to GPT-4, one of the most expensive models.

Let's find out if we can get away with a cheaper/faster model. Most models cannot handle the number of tokens needed to ingest a whole wikipedia article, so we'll turn to the two that can that are also cheaper than GPT4: Claude 3 Sonnet and Claude 3 Haiku.

```python
from superpipe.grid_search import GridSearch
from superpipe.models import claude3_haiku, claude3_sonnet
from superpipe.steps import LLMStructuredCompositeStep

# we need to use LLMStructuredCompositeStep which uses GPT3.5 for structured JSON extraction
# because Claude does not support JSON mode or function calling out of the box
new_extract_step = LLMStructuredCompositeStep(
  model=models.claude3_haiku,
  prompt=extract_step.prompt,
  out_schema=ExtractedData,
  name="extract_data_new"
)

new_pipeline = Pipeline([
  search_step,
  parse_search_step,
  fetch_wikipedia_step,
  new_extract_step
], evaluation_fn=eval_fn)

param_grid = {
  new_extract_step.name:{
    "model": [claude3_haiku, claude3_sonnet]}
}
grid_search = GridSearch(new_pipeline, param_grid)
grid_search.run(df)
```

<p align="center"><img src="../assets/wikipedia_gridsearch.png" style="width: 800px;" /></p>

```python
best_params = grid_search.best_params
new_pipeline.update_params(best_params)
new_pipeline.run(df)
print("Score: ", new_pipeline.score)
for step in new_pipeline.steps:
  print(f"Step {step.name}:")
  print(f"- Latency: {step.statistics.total_latency}")
  print(f"- Cost: {step.statistics.input_cost + step.statistics.output_cost}")
```

## Next Steps

[**Concepts**](../concepts) &mdash; to understand the core concepts behind Superpipe in more depth.

[**Why Superpipe?**](../why) &mdash; to understand whether Superpipe is right for you.

[**Examples**](../examples) &mdash; for more advanced examples and usage.
