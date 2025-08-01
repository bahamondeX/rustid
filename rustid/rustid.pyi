"""
High-performance UUID generation library with enhanced features.

This module provides a drop-in replacement for Python's uuid module
with significant performance improvements through Rust implementation.
"""

from typing import Optional, List, Union

class UUID:
    """
    A universally unique identifier with enhanced performance.
    
    Drop-in replacement for uuid.UUID with additional methods for
    short IDs and base64 encoding.
    """
    
    def __init__(
        self, 
        hex: Optional[str] = None, 
        bytes: Optional[bytes] = None
    ) -> None:
        """
        Create a UUID from a hex string or bytes.
        
        Args:
            hex: 32-character hexadecimal string (with or without hyphens)
            bytes: 16-byte sequence
            
        Raises:
            ValueError: If hex string is invalid or bytes length != 16
        """
        ...
    
    @property
    def hex(self) -> str:
        """32-character lowercase hexadecimal string without hyphens."""
        ...
    
    @property
    def bytes(self) -> bytes:
        """16-byte representation of the UUID."""
        ...
    
    @property
    def version(self) -> int:
        """UUID version number (1, 4, or 7)."""
        ...
    
    @property
    def variant(self) -> str:
        """UUID variant specification."""
        ...
    
    def short_id(self) -> str:
        """
        Generate a 16-character URL-safe short ID from this UUID.
        
        Returns:
            16-character base64-encoded string (URL-safe, no padding)
        """
        ...
    
    def base64(self) -> str:
        """
        Generate a base64 representation of the UUID.
        
        Returns:
            22-character base64-encoded string
        """
        ...
    
    def int(self) -> int:
        """
        Integer representation of the UUID.
        
        Returns:
            128-bit integer
        """
        ...
    
    def __str__(self) -> str:
        """Standard UUID string format with hyphens."""
        ...
    
    def __repr__(self) -> str:
        """Representation showing UUID constructor call."""
        ...
    
    def __eq__(self, other: object) -> bool:
        """Compare UUIDs for equality."""
        ...
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries."""
        ...

def uuid1() -> UUID:
    """
    Generate a UUID based on host MAC address and timestamp.
    
    Returns:
        UUID version 1
    """
    ...

def uuid4() -> UUID:
    """
    Generate a random UUID.
    
    Returns:
        UUID version 4 (random)
    """
    ...

def uuid7() -> UUID:
    """
    Generate a time-ordered UUID with millisecond precision.
    
    Returns:
        UUID version 7 (time-ordered)
    """
    ...

def uuid4_batch(count: int) -> List[UUID]:
    """
    Generate multiple random UUIDs in parallel.
    
    Args:
        count: Number of UUIDs to generate
        
    Returns:
        List of UUID version 4 objects
    """
    ...

def uuid7_batch(count: int) -> List[UUID]:
    """
    Generate multiple time-ordered UUIDs in parallel.
    
    Args:
        count: Number of UUIDs to generate
        
    Returns:
        List of UUID version 7 objects
    """
    ...

def short_id() -> str:
    """
    Generate a 16-character URL-safe time-sortable ID.
    
    Based on UUID v7 truncated to 12 bytes and base64-encoded.
    Maintains time-ordering properties while being URL-safe.
    
    Returns:
        16-character URL-safe string
    """
    ...

def short_id_batch(count: int) -> List[str]:
    """
    Generate multiple short IDs in parallel.
    
    Args:
        count: Number of short IDs to generate
        
    Returns:
        List of 16-character URL-safe strings
    """
    ...

def nano_id(size: Optional[int] = None) -> str:
    """
    Generate a NanoID - URL-safe unique string identifier.
    
    Uses alphabet: 0-9A-Za-z-_ (64 characters)
    Default size provides ~132 years of collision resistance
    at 1000 IDs/hour.
    
    Args:
        size: Length of the generated ID (default: 21)
        
    Returns:
        URL-safe unique identifier string
    """
    ...

def nano_id_batch(count: int, size: Optional[int] = None) -> List[str]:
    """
    Generate multiple NanoIDs in parallel.
    
    Args:
        count: Number of NanoIDs to generate
        size: Length of each ID (default: 21)
        
    Returns:
        List of URL-safe unique identifier strings
    """
    ...

# Compatibility aliases
NAMESPACE_DNS: UUID
NAMESPACE_URL: UUID
NAMESPACE_OID: UUID
NAMESPACE_X500: UUID

# Version constants
__version__: str