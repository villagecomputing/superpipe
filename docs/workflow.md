# Superpipe Workflow

## Build, eval, optimize

There are three stages of using Superpipe.

1. **Building** a pipeline
2. **Evaluating** your pipeline
3. **Optimizing** your pipeline

### Build

Any multistep LLM workflow can be converted to a Superpipe pipeline.

Take a look at our [concepts page](../concepts) for a better understanding of Superpipe concepts.

Before you can start using Superpipe you need:

- **A well defined task** - Superpipe is designed well defined tasks like categorization, tagging, and extraction. You should know your goal before you get started.
- **Input Data** - the dataset you want to transform with your pipeline. Superpipe acts over Pandas Dataframes or dictionaries.

With that in hand, you will use Superpipe to build:

- **[Steps](../concepts/steps/)** - each step takes in an input dataframe or Python dictionary and returns a new dataframe or dictionary with the outputs of the step appended.
- **[Pipeline](../concepts/pipelines)** - steps are chained together to create a pipeline.

### Evaluate

Once you've built your pipeline it's time to see how well it works. This requires:

- **Evaluation function** - a function that defines what "correct" is. In many cases this is a string comparison with your ground truth labels but could be any arbitrary function, including a call to an LLM to evaluate generative outputs.
- **Ground truth labels** - the _correct_ label for each row in your data. You can use an early version of your pipeline to generate _candidate labels_ and manually inspect and correct to generate your ground truth.

### Optimize

The last step in using Superpipe is trying out many permutations of step paramaters to optimize your pipeline along **cost, accuracy, and speed**.

For example, you may want to try:

- GPT-4 vs. Mixtral
- 3, 5, 7 retrieval chunks
- Chain of thought vs. direct prompting
- Few shot prompts

One of the core principles of Superpipe is that you should build once, experiment many times. By building your pipeline in Superpipe steps, testing out every paramater permutation is trivial.

Pipeline optimization is done via a [grid search](../concepts/grid_search).

A common usecase of Superpipe is understanding if you can "get away" with using an open source model. See the [models](../concepts/models) to learn how to use Superpipe with any LLM model from any provider.

## The Superpipe process

- Read in your data
- Define your [steps](../concepts/steps)
- Combine steps and eval function into a [pipeline](../concepts/pipelines)
- Test your pipeline and generate _candidate ground truth_
- Manually inspect and correct your ground truth
- Define an evaluation function
- Define a grid search paramater dictionary
- Run a grid search
- ...profit
