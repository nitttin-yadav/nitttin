"""Comprehensive tests for the string_utils module."""

import pytest

from nitttin.string_utils import (
    reverse,
    is_palindrome,
    capitalize_words,
    count_vowels,
    count_consonants,
    truncate,
    snake_to_camel,
    camel_to_snake,
)


class TestReverse:
    def test_word(self):
        assert reverse("hello") == "olleh"

    def test_empty(self):
        assert reverse("") == ""

    def test_single_char(self):
        assert reverse("x") == "x"


class TestIsPalindrome:
    def test_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False


class TestCapitalizeWords:
    def test_basic(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_already_capitalized(self):
        assert capitalize_words("Hello") == "Hello"

    def test_single_word(self):
        assert capitalize_words("python") == "Python"


class TestCountVowels:
    def test_basic(self):
        assert count_vowels("hello") == 2

    def test_all_vowels(self):
        assert count_vowels("aeiou") == 5

    def test_no_vowels(self):
        assert count_vowels("rhythm") == 0


class TestCountConsonants:
    def test_basic(self):
        assert count_consonants("hello") == 3

    def test_no_consonants(self):
        assert count_consonants("aeiou") == 0

    def test_with_spaces(self):
        assert count_consonants("hi there") == 4


class TestTruncate:
    def test_short_string_not_truncated(self):
        assert truncate("hi", 10) == "hi"

    def test_long_string_truncated(self):
        assert truncate("hello world", 8) == "hello..."

    def test_custom_suffix(self):
        assert truncate("hello world", 7, suffix="~") == "hello ~"

    def test_max_length_too_small_raises(self):
        with pytest.raises(ValueError, match="max_length must be at least"):
            truncate("hello", 2, suffix="...")


class TestSnakeToCamel:
    def test_basic(self):
        assert snake_to_camel("hello_world") == "helloWorld"

    def test_single_word(self):
        assert snake_to_camel("hello") == "hello"

    def test_multiple_parts(self):
        assert snake_to_camel("one_two_three") == "oneTwoThree"


class TestCamelToSnake:
    def test_basic(self):
        assert camel_to_snake("helloWorld") == "hello_world"

    def test_single_word(self):
        assert camel_to_snake("hello") == "hello"

    def test_multiple_humps(self):
        assert camel_to_snake("oneTwoThree") == "one_two_three"
