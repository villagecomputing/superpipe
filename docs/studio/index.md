# Superpipe Studio

Superpipe Studio is a free and open-source observability and experimentation app for the Superpipe SDK. It can help you:

- **Log and monitor results of your Superpipe pipelines in dev or production**
- **Manage datasets and build golden sets for ground truth labeling and evaluation**
- **Track experiments/grid searches and compare them on accuracy, latency and cost**

Superpipe Studio is a Next JS app that can be run locally or self-hosted with Vercel.

**Demo**

<div style="position: relative; padding-bottom: 67.5%; height: 0;"><iframe width="560" height="315" src="https://www.youtube.com/embed/fKKmUm12LDY?si=Qj1mjtoStpdjG6PU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>

## Running Superpipe Studio

To run Superpipe Studio locally follow instructions in [Running Studio locally](https://github.com/villagecomputing/studio/tree/aman/more-readme?tab=readme-ov-file#running-studio-locally) or to self-host with Vercel follow instructions in [Deplying Studio with Vercel](https://github.com/villagecomputing/studio/tree/aman/more-readme?tab=readme-ov-file#deploying-studio-with-vercel).

## Usage with Superpipe

1. Install the superpipe-studio python library with `pip install superpipe-studio`. Also make sure you're on the latest version of superpipe (`pip install superpipe-py -U`).
2. Set the following environment variables:
   1. `SUPERPIPE_STUDIO_URL` = the url where your studio instance is hosted
   2. `SUPERPIPE_API_KEY` = your Superpipe API key if running Studio with authentication enabled (see the [Authenticating Superpipe Studio requests](https://github.com/villagecomputing/studio/tree/aman/more-readme?tab=readme-ov-file#authenticating-superpipe-sdk-requests) section of the Studio readme)

### Logging

To log a pipeline to Studio, simply pass in `enable_logging=True` when calling `pipeline.run`.

```python
input = {
  ...
}
pipeline.run(data=input, enable_logging=True)
```

It’s helpful to set the pipeline’s `name` field when initializing it to identify the pipeline logs in Studio.

### Datasets

Creating a Studio dataset uploads the data to Studio where you can visualize it in a convenient interface. It also allows you to use the same dataset across experiments.

Datasets are created by calling the constructor of the `Dataset` class and passing in a pandas dataframe.

```python
from studio import Dataset
import pandas as pd

df = pd.DataFrame(...)
dataset = Dataset(data=df, name="furniture")
```

**Ground truth columns**

You can optionally specify a list of ground truth columns which will be shown separately in the Studio UI and can be edited. This lets you create datasets with accurate ground truth labels that can be used to evaluate your pipelines.

```python
dataset = Dataset(data=df, name="furniture", ground_truths=["brand_name"])
```

You can also download a dataset that already exists in Studio by passing in its `id`.

```python
id = dataset.id
dataset_copy = Dataset(id=id)
```

To add data to an existing dataset, call the `add_data` function on a dataset and pass in a pandas dataframe.

```python
df = pd.DataFrame(...)
dataset.add_data(data=df)
```

### Experiments

Experiments in Studio help you log the results of running a pipeline or a grid search on a dataset, so you can evaluate their accuracy, cost and speed and compare pipelines objectively.

To run a pipeline experiment, define your pipeline as usual, call `pipeline.run_experiment` and pass in a pandas dataframe, a Studio dataset object or a dataset id string. If you pass in a dataframe, a Studio dataset object will be created and can be reused for future experiments. If you pass in a dataset id, a Studio dataset will be downloaded.

```python
import pandas as pd
from studio import Dataset

# running an experiment on a dataframe implicitly creates a new dataset
df = pd.DataFrame(...)
pipeline.run_experiment(data=df)

# running an experiment on an existing dataset
dataset = Dataset(data=df, name="furniture")
pipeline.run_experiment(data=dataset)
```

To run a grid search experiment, define your grid search as usual, call `grid_search.run_experiment`. Everything else is the same as a pipeline experiment, but you will see one experiment created for each set of parameters in the grid search.

```python
grid_search.run_experiment(data=df)
```

**Experiment groups**

Studio intelligently groups pipeline experiments so you can compare them more easily. Two experiments will be added to the same group if:

1. they have the same name, and
2. they have the same steps (but the steps can have different params)

Grid searches are automatically grouped into the same experiment group.

## Usage without Superpipe

Studio can be used even if you're not using Superpipe to build your LLM pipelines.

You can interact with Studio directly via REST API - see [API docs here](https://superpipe.vercel.app/api-doc).
