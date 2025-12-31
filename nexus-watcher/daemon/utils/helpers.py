"""Helper utilities for Nexus Watcher daemon."""

import hashlib
import json
from typing import Any, Dict
from datetime import datetime
from urllib.parse import urlparse


def calculate_hash(data: Any) -> str:
    """
    Calculate SHA256 hash of data.

    Args:
        data: Data to hash (will be JSON serialized)

    Returns:
        Hex digest of hash
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True)
    elif not isinstance(data, (str, bytes)):
        data = str(data)

    if isinstance(data, str):
        data = data.encode('utf-8')

    return hashlib.sha256(data).hexdigest()


def validate_url(url: str) -> bool:
    """
    Validate if string is a valid URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: URL string

    Returns:
        Domain name or empty string
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""


def timestamp_iso() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp
    """
    return datetime.utcnow().isoformat() + 'Z'


def safe_get(data: Dict, key_path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.

    Args:
        data: Dictionary to search
        key_path: Dot-separated key path (e.g., 'auth.method')
        default: Default value if key not found

    Returns:
        Value or default
    """
    keys = key_path.split('.')
    value = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default

    return value


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to max length.

    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
