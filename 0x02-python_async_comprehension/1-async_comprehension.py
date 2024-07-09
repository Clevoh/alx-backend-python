#!/usr/bin/env python3
"""Async Comprehensions"""

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """collect 10 random numbers over async_generator and return random numbers"""
    random_returns = [i async for i in async_generator()]
    return random_returns
