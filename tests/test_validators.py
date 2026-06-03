"""Comprehensive tests for the validators module."""

import pytest

from nitttin.validators import (
    is_valid_email,
    is_valid_url,
    is_valid_phone,
    is_strong_password,
    is_valid_ip,
    is_valid_credit_card,
)


class TestIsValidEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "first.last@domain.org",
            "user+tag@sub.domain.co",
            "name123@test.io",
        ],
    )
    def test_valid_emails(self, email):
        assert is_valid_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "",
            "plaintext",
            "@domain.com",
            "user@",
            "user@.com",
            "user@domain",
            "user @domain.com",
        ],
    )
    def test_invalid_emails(self, email):
        assert is_valid_email(email) is False


class TestIsValidUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "http://example.com",
            "https://www.google.com",
            "https://sub.domain.co/path",
            "http://test.io/a/b/c",
        ],
    )
    def test_valid_urls(self, url):
        assert is_valid_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "",
            "ftp://example.com",
            "example.com",
            "http://",
            "://missing-scheme.com",
        ],
    )
    def test_invalid_urls(self, url):
        assert is_valid_url(url) is False


class TestIsValidPhone:
    @pytest.mark.parametrize(
        "phone",
        [
            "1234567890",
            "123-456-7890",
            "(123) 456-7890",
            "+1 123-456-7890",
            "123.456.7890",
        ],
    )
    def test_valid_phones(self, phone):
        assert is_valid_phone(phone) is True

    @pytest.mark.parametrize(
        "phone",
        [
            "",
            "123",
            "abcdefghij",
            "12345",
            "123-456-789",
        ],
    )
    def test_invalid_phones(self, phone):
        assert is_valid_phone(phone) is False


class TestIsStrongPassword:
    @pytest.mark.parametrize(
        "password",
        [
            "Str0ng!Pass",
            "C0mpl3x@Password",
            "Abc12345!",
        ],
    )
    def test_strong_passwords(self, password):
        assert is_strong_password(password) is True

    def test_too_short(self):
        assert is_strong_password("Ab1!") is False

    def test_no_uppercase(self):
        assert is_strong_password("abcdefg1!") is False

    def test_no_lowercase(self):
        assert is_strong_password("ABCDEFG1!") is False

    def test_no_digit(self):
        assert is_strong_password("Abcdefg!!") is False

    def test_no_special_char(self):
        assert is_strong_password("Abcdefg12") is False


class TestIsValidIp:
    @pytest.mark.parametrize(
        "ip",
        [
            "0.0.0.0",
            "192.168.1.1",
            "255.255.255.255",
            "10.0.0.1",
        ],
    )
    def test_valid_ips(self, ip):
        assert is_valid_ip(ip) is True

    @pytest.mark.parametrize(
        "ip",
        [
            "",
            "256.0.0.1",
            "1.2.3",
            "1.2.3.4.5",
            "01.02.03.04",
            "abc.def.ghi.jkl",
            "-1.0.0.0",
        ],
    )
    def test_invalid_ips(self, ip):
        assert is_valid_ip(ip) is False


class TestIsValidCreditCard:
    @pytest.mark.parametrize(
        "number",
        [
            "4111111111111111",  # Visa test number
            "4111 1111 1111 1111",
            "4111-1111-1111-1111",
            "5500000000000004",  # Mastercard test number
        ],
    )
    def test_valid_cards(self, number):
        assert is_valid_credit_card(number) is True

    @pytest.mark.parametrize(
        "number",
        [
            "",
            "1234",
            "abcdefghijklmno",
            "1234567890123456",
            "9999999999999999",
        ],
    )
    def test_invalid_cards(self, number):
        assert is_valid_credit_card(number) is False
