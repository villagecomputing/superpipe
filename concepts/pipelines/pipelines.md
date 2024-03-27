# Pipelines

Pipelines are the engines that make Superpipe run. A pipeline is a series of steps chained together that acts on a dataframe. A pipeline takes an optional evaluation function that can run arbitrary Python code. Evaluation functions need to return booleans.

## Pipeline statistics

A pipeline object has associated pipeline statistics.

| Stat          | Description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| score         | Accuracy score of the pipeline as defined by the evaluation function.  |
| input_tokens  | Total number of input tokens used by the pipeline split out by model.  |
| output_tokens | Total number of output tokens used by the pipeline split out by model. |
| input_cost    | Total input cost of the pipeline split out by model.                   |
| output_cost   | Total output cost of the pipeline split out by model.                  |
| num_success   | Number of successful rows.                                             |
| num_failure   | Number of unsuccessful rows.                                            |
| total_latency | Total latency of the pipeline.                                         |

## Pipeline methods

### update_param()

`pipeline.update_params()` takes a parameters dictionary of steps and parameters.
For example, to update the `categorize` pipeline to use GPT-4, we can call `update_param` and pass in the step name as the key, with a sub dictionary with model as the key.

```python
categorizer.update_params({
  "categorize": {
    "model": models.gpt4
  }
})
```

## Example

You can find the full code for this example in the [comparing pipelines](../examples/comparing_pipelines/furniture.ipynb) example. This is just the pipeline definition.

```python
evaluate = lambda row: row['predicted_category'].lower() == row['category_new'].lower()

categorizer = pipeline.Pipeline([
  short_description_step,
  embedding_search_step,
  categorize_step,
  select_category_step
], evaluation_fn=evaluate)

categorizer.run(test_df)
```
