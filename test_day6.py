
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from orders import check_order
import support


class TestCustomerSupportTools(unittest.TestCase):

    def test_existing_order(self):
        result = check_order("TS1001")

        self.assertIn("TS1001", result)
        self.assertIn("Laptop", result)
        self.assertIn("Shipped", result)

    def test_second_order(self):
        result = check_order("TS1002")

        self.assertIn("Headphones", result)
        self.assertIn("Processing", result)

    def test_unknown_order(self):
        result = check_order("TS9999")

        self.assertIn("not found", result.lower())

    def test_escalation_creates_ticket(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_escalations.txt"

            with patch.object(support, "TICKET_FILE", test_file):
                result = support.create_support_ticket(
                    issue="Product arrived damaged",
                    order_id="TS1001",
                )

            self.assertIn("Ticket ID:", result)
            self.assertTrue(test_file.exists())

            saved_ticket = test_file.read_text(encoding="utf-8")

            self.assertIn("Product arrived damaged", saved_ticket)
            self.assertIn("TS1001", saved_ticket)

    def test_escalation_does_not_claim_notification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_escalations.txt"

            with patch.object(support, "TICKET_FILE", test_file):
                result = support.create_support_ticket(
                    issue="Refund issue"
                )

            self.assertIn("has not yet been notified", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
