"""
rustid - High-performance UUID generation with enhanced features.

This module provides a drop-in replacement for Python's uuid module
with significant performance improvements through Rust implementation.
"""

from .rustid import (
    UUID,
    uuid1,
    uuid4,
    uuid7,
    uuid4_batch,
    uuid7_batch,
    short_id,
    short_id_batch,
    nano_id,
    nano_id_batch,
)

# Compatibility with Python's uuid module
from uuid import NAMESPACE_DNS, NAMESPACE_URL, NAMESPACE_OID, NAMESPACE_X500

__version__ = "0.0.1"
__all__ = [
    "UUID",
    "uuid1", 
    "uuid4",
    "uuid7",
    "uuid4_batch",
    "uuid7_batch", 
    "short_id",
    "short_id_batch",
    "nano_id",
    "nano_id_batch",
    "NAMESPACE_DNS",
    "NAMESPACE_URL", 
    "NAMESPACE_OID",
    "NAMESPACE_X500",
]