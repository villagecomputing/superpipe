# Why superpipe?

There are several great tools that help you chain together LLM calls or build agent workflows that make for great prototypes or demos. Superpipe is different for two reasons:

**It focuses exclusively on unstructured -> structured (extraction and classification) problems.** Though it can be used for generative use cases, that is not where it shines.

**It helps you evaluate and optimize across accuracy, speed and cost.** Accuracy, speed and cost don't matter for prototypes and demos, but they do when you're trying to solve real problems for real customers at scale.

Superpipe does not pretend to do everything, it does a few things and does them well.

## When to use Superpipe

!!! note "Superpipe is a good choice if your use case has some or most of these properties"

    1. You primarily care about structured output, not generative output.
    2. You care about evaluating your pipeline on a ground truth dataset (you may or may not already have labels).
    3. You care about finding the best combination of accuracy, cost and speed for your use case.
    4. You need to monitor your pipeline in production to prevent model drift and data drift.
    5. You want to continuously increase accuracy and decrease cost/speed as new models and techniques come out.
    6. You want to use your production data to create fine-tuned or use-case specific models.

## When NOT to use Superpipe

!!! note "Superpipe is not a good choice if"

    1. You're working on generative, chat-like, or agentic use cases.
    1. You're building a demo or prototype.
    2. You just need to build something good enough and don't need to optimize across accuracy, cost and speed.

## Workflow for building production-grade LLM pipelines

_To build production-grade LLM pipelines, software engineers need to think like scientists._

In a general unstructured -> structured problem, you're given some unstructured data (text, website, pdf, image, etc.) Your task is to extract, transform, or classify each data point into some structure that's known ahead of time. You may have pre-existing ground truth labels (`supervised learning`) or not (`unsupervised learning`)

#### 1. Build the first version of your pipeline

Superpipe can help you build the first version of your pipeline, but you can also use your favorite LLM library (like langchain or LlamaIndex), make API calls, use an embedding provider, etc.

Regardless of what you use to define the logic, it helps to break your pipeline into logically separate steps and wrap them inside the Superpipe `CustomStep` class. [See why here](./using/steps/CustomStep.md).

#### 2. Label your data using the pipeline (if ground truth labels aren't provided)

If you already have (high-quality) ground truth labels, you can skip this step. Otherwise you will need to create these labels to evaluate against. To do this we recommend

- using the highest quality models available (currently GPT-4 and Claude 3 Opus) and the most powerful techniques to build your pipeline (Step 1).
- validating and correcting the labels manually ([Superpipe Studio](./studio/) can help with this).

#### 3. Try different techniques/parameters and evaluate them against each other with a grid search

Now try switching to less powerful models to reduce cost and increase speed, while accuracy remains acceptably high compared to the more powerful model you used in Step 1.

Superpipe makes it easy to swap out different models for each step and tweak the parameters of each step while easily evaluating each parameter choice on the same dataset. See the [Optimization](/) section and the [Grid Search](./using/grid_search.md) page.

Pick the approach and parameters that make the best accuracy-cost-speed tradeoff for your situation.

#### 4. Deploy to production, collect more data to finetune an existing or pretrain a custom model

Build and deploy the best pipeline to production and start serving real requests. If you built your pipeline with Superpipe and plug it into Superpipe Studio, you will automatically start collecting data which can be used for:

- fine-tuning an open source model or training a new one
- running experiments with new models as they come out or with more advanced pipeline approaches
- backtesting all of the above on real data, or trying it on live data in shadow mode
