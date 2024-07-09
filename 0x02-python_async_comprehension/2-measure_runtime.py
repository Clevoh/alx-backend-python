#!/usr/bin/env python3
"""Measure runtime for four parallel comprehensions"""

from asyncio import gather
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """run async_comprehension 4 times, measure and return elapsed time"""
    start = time.time()
    functions_run = [async_comprehension() for _ in range(4)]
    await gather(*functions_run)
    end = time.time() - start
    return end
