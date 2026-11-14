
def compare_algorithms(results):
    """
    Compare the results of multiple graph coloring algorithms.

    Expected input:
    {
        "Backtracking": {
            "success": True,
            "chromatic_number": 3,
            "execution_time": 0.002
        },
        "Genetic Algorithm": {
            "success": True,
            "chromatic_number": 4,
            "execution_time": 0.01
        }
    }
    """

    if not isinstance(results, dict):
        raise TypeError("Results must be a dictionary.")

    comparison = {}

    for algorithm, result in results.items():

        if not isinstance(result, dict):
            continue

        success = result.get("success", False)
        chromatic_number = result.get("chromatic_number")
        execution_time = result.get("execution_time")

        comparison[algorithm] = {
            "success": success,
            "chromatic_number": (
                chromatic_number
                if isinstance(chromatic_number, int)
                and not isinstance(chromatic_number, bool)
                and chromatic_number >= 0
                else None
            ),
            "execution_time": (
                execution_time
                if isinstance(execution_time, (int, float))
                and not isinstance(execution_time, bool)
                and execution_time >= 0
                else None
            )
        }

    return comparison


def get_best_algorithm(comparison):
    """
    Find the best successful algorithm.

    Priority:
    1. Lowest chromatic number.
    2. Lowest execution time when chromatic numbers are equal.
    """

    valid_results = []

    for algorithm, result in comparison.items():

        if not result.get("success", False):
            continue

        chromatic_number = result.get("chromatic_number")
        execution_time = result.get("execution_time")

        if chromatic_number is None:
            continue

        if execution_time is None:
            continue

        valid_results.append(
            (algorithm, chromatic_number, execution_time)
        )

    if not valid_results:
        return None

    best = min(
        valid_results,
        key=lambda item: (item[1], item[2])
    )

    return {
        "algorithm": best[0],
        "chromatic_number": best[1],
        "execution_time": best[2]
    }


def get_comparison_summary(comparison):
    """
    Return a summary of the comparison results.
    """

    total = len(comparison)

    successful = sum(
        1
        for result in comparison.values()
        if result.get("success", False)
    )

    best_algorithm = get_best_algorithm(comparison)

    return {
        "total_algorithms": total,
        "successful_algorithms": successful,
        "failed_algorithms": total - successful,
        "best_algorithm": best_algorithm
    }
