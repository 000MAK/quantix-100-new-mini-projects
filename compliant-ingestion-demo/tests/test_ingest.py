from __future__ import annotations

import unittest

from ingest import pseudonymous_reference, validate_row


POLICY = {
    "authorized_source_values": ["true", "yes", "1"],
    "allowed_consent_statuses": ["granted", "explicit_opt_in"],
}


def valid_row() -> dict[str, str]:
    return {
        "record_id": "synthetic-person-001",
        "source": "example_partner_feed",
        "source_authorized": "true",
        "consent_status": "granted",
        "locale": "en-US",
        "currency": "USD",
        "email": "this-field-must-not-be-exported@example.invalid",
    }


class IngestionPolicyTests(unittest.TestCase):
    def test_valid_authorized_consented_row_is_minimized(self) -> None:
        ok, reason, output = validate_row(valid_row(), POLICY)
        self.assertTrue(ok)
        self.assertEqual(reason, "accepted")
        self.assertIsNotNone(output)
        self.assertEqual(
            set(output or {}),
            {"record_id", "source", "locale", "currency"},
        )
        self.assertNotIn("email", output or {})

    def test_unauthorized_source_is_rejected(self) -> None:
        row = valid_row()
        row["source_authorized"] = "false"
        ok, reason, output = validate_row(row, POLICY)
        self.assertFalse(ok)
        self.assertEqual(reason, "source_not_authorized")
        self.assertIsNone(output)

    def test_missing_consent_is_rejected(self) -> None:
        row = valid_row()
        row["consent_status"] = "unknown"
        ok, reason, output = validate_row(row, POLICY)
        self.assertFalse(ok)
        self.assertEqual(reason, "consent_missing_or_not_allowed")
        self.assertIsNone(output)

    def test_invalid_locale_or_currency_is_rejected(self) -> None:
        row = valid_row()
        row["locale"] = "not a locale!"
        ok, reason, output = validate_row(row, POLICY)
        self.assertFalse(ok)
        self.assertEqual(reason, "invalid_locale")
        self.assertIsNone(output)

        row = valid_row()
        row["currency"] = "US dollars"
        ok, reason, output = validate_row(row, POLICY)
        self.assertFalse(ok)
        self.assertEqual(reason, "invalid_currency")
        self.assertIsNone(output)

    def test_hmac_reference_does_not_equal_raw_identifier(self) -> None:
        result = pseudonymous_reference("internal-123", b"x" * 32)
        self.assertEqual(len(result), 24)
        self.assertNotIn("internal-123", result)


if __name__ == "__main__":
    unittest.main()
