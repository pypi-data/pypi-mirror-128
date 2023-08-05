"""Functions for checking and flattening multidimensional lists."""
from typing import List


def ensure2d(lst: List) -> bool:
    """Make sure the list is a 2d list."""
    for element in lst:
        if not isinstance(element, list):
            return False
        for inner_element in element:
            if isinstance(inner_element, list):
                return False
    return True


def deepflatten(lst: List) -> List:
    """Flatten a list with unknown depth into a 1d list."""
    flatted = []
    for element in lst:
        if isinstance(element, list):
            flatted = deepflatten(element) + flatted
        else:
            flatted.append(element)
    return flatted


def flatten2d(lst: List) -> List:
    """Flatten a 2d list into a 1d list."""
    flatted = []
    for element in lst:
        if isinstance(element, list):
            for inner_element in element:
                flatted.append(inner_element)
        else:
            flatted.append(element)
    return flatted
