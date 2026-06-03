"""String manipulation utilities."""


def reverse(s: str) -> str:
    """Return the reversed string."""
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word."""
    return " ".join(word.capitalize() for word in s.split())


def count_vowels(s: str) -> int:
    """Count the number of vowels in a string."""
    return sum(1 for char in s.lower() if char in "aeiou")


def count_consonants(s: str) -> int:
    """Count the number of consonants in a string."""
    return sum(1 for char in s.lower() if char.isalpha() and char not in "aeiou")


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to max_length, appending suffix if truncated.

    Raises:
        ValueError: If max_length is less than the length of suffix.
    """
    if max_length < len(suffix):
        raise ValueError("max_length must be at least as long as suffix")
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def snake_to_camel(s: str) -> str:
    """Convert a snake_case string to camelCase."""
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def camel_to_snake(s: str) -> str:
    """Convert a camelCase string to snake_case."""
    result = []
    for i, char in enumerate(s):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)
