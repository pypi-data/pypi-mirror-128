import operator
from typing import Tuple, Iterable, List, Set


def get_all_available_major_version(versions: Iterable[List[int]]) -> List[Tuple[str, str]]:
    all_version: Set[tuple] = set()
    for version in versions:
        all_version.add((f'{version[0]}.', f'{version[0]}.x.x'))
        all_version.add((f'{version[0]}.{version[1]}.', f'{version[0]}.{version[1]}.x'))
    return sorted((version for version in all_version), key=operator.itemgetter(1))
