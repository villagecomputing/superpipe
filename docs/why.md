# Why Superpipe?

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
