from typing import List


def deepflat(lst: List) -> List:
    """Flatten a list with unknown depth into a 1d list."""
    flatted = []
    for element in lst:
        if isinstance(element, list):
            flatted = deepflat(element) + flatted
        else:
            flatted.append(element)
    return flatted
