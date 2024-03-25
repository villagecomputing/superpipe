import time
from functools import wraps
from superpipe.steps.step import StepRowStatistics
from typing import List


class ShouldNotInterrupt(Exception):
    """
    Exception that indicates a process should not be interrupted.
    """
    pass


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
        try:
            start_time = time.time()
            result = fn(*args, **kwargs)
            success = True
        except ShouldNotInterrupt:
            result = None
            success = False
        except Exception as e:
            success = False
            raise e
        finally:
            end_time = time.time()
            latency = end_time - start_time
            statistics = StepRowStatistics(latency=latency, success=success)
        return result, statistics

    return wrapper


def combine_step_row_statistics(statistics_list: List[StepRowStatistics]) -> StepRowStatistics:
    """
    Combines a list of StepRowStatistics into a single StepRowStatistics object.

    Args:
        statistics_list (List[StepRowStatistics]): A list of StepRowStatistics objects.

    Returns:
        StepRowStatistics: The combined statistics.
    """
    input_tokens = sum(stat.input_tokens for stat in statistics_list)
    output_tokens = sum(stat.output_tokens for stat in statistics_list)
    success = all(stat.success for stat in statistics_list)
    latency = sum(stat.latency for stat in statistics_list)
    input_cost = sum(stat.input_cost for stat in statistics_list)
    output_cost = sum(stat.output_cost for stat in statistics_list)
    return StepRowStatistics(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        success=success,
        latency=latency,
        input_cost=input_cost,
        output_cost=output_cost
    )
