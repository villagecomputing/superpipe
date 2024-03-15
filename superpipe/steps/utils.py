import time
from functools import wraps
from superpipe.steps.step import StepRowStatistics


def with_statistics(fn):
    """
    Decorator for adding statistics to a step's transformation function.

    Args:
        fn (Callable): The transformation function to decorate.

    Returns:
        Callable: The decorated transformation function.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        """
        Applies the transformation function to a single row of data and updates the step's statistics.
        """
        start_time = time.time()
        result = fn(*args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        statistics = StepRowStatistics(latency=latency)
        return result, statistics

    return wrapper
