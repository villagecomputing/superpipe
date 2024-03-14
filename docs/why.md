# Why superpipe?

Superpipe does not pretend to do everything, it does a few things and does them well.

!!! note "Superpipe is a good choice if your use case has some or most of these properties"

    1. You primarily care about structured output, not generative output.
    2. You care about generating a high-quality ground truth dataset and evaluating your pipeline on it.
    3. You care about finding the best combination of accuracy, cost and speed for your use case.
    4. You need to monitor your pipeline in production to prevent model drift and data drift.
    5. You want to continuously increase accuracy and decrease cost/speed as new models and techniques come out.
    6. You want to use your production data to create fine-tuned or use-case specific models.

!!! note "Superpipe is not a good choice if"

    1. You're building a demo or prototype.
    2. You just need to get something out there that's good enough, and don't need to optimize across accuracy, cost and speed.
