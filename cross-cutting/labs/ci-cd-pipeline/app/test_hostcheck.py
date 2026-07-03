#!/usr/bin/env python3
"""Tests for hostcheck — the thing CI runs on every push. Pure stdlib unittest,
so `python3 -m unittest` needs no pip install."""

import unittest

from hostcheck import is_valid, normalize


class TestNormalize(unittest.TestCase):
    def test_trims_and_lowercases(self):
        self.assertEqual(normalize("  Web01.PROD  "), "web01.prod")

    def test_already_clean(self):
        self.assertEqual(normalize("db-1.internal"), "db-1.internal")


class TestIsValid(unittest.TestCase):
    def test_accepts_normal_hostnames(self):
        for h in ["web01", "db-1.internal", "a.b.c", "host-9.example.com",
                  "  Web01.PROD  "]:  # normalized before validation
            self.assertTrue(is_valid(h), f"{h!r} should be valid")

    def test_rejects_empty_and_whitespace(self):
        for h in ["", "   ", "\t"]:
            self.assertFalse(is_valid(h), f"{h!r} should be invalid")

    def test_rejects_bad_characters(self):
        for h in ["under_score", "space here", "bang!", "café"]:
            self.assertFalse(is_valid(h), f"{h!r} should be invalid")

    def test_rejects_leading_or_trailing_hyphen(self):
        for h in ["-lead", "trail-", "a.-b", "a.b-"]:
            self.assertFalse(is_valid(h), f"{h!r} should be invalid")

    def test_rejects_oversized_label(self):
        self.assertFalse(is_valid("a" * 64))          # label > 63
        self.assertTrue(is_valid("a" * 63))           # label == 63 is fine

    def test_rejects_oversized_hostname(self):
        long = ".".join(["abc"] * 80)                 # > 253 chars total
        self.assertFalse(is_valid(long))


if __name__ == "__main__":
    unittest.main()
