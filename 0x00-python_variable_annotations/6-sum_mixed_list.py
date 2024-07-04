#!/usr/bin/env python3
"""Type-annotated function sum_mixed_list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """takes a mixed list of int and floats and returns
        their sum as float"""
    a: float = 0.0
    for x in mxd_lst:
        a += x
    return a
