
from pathlib import Path
from uuid import uuid4
from datetime import datetime


PROJECT_DIR = Path(__file__).resolve().parent
TICKET_FILE = PROJECT_DIR / "escalations.txt"


def create_support_ticket(issue: str, order_id: str = "Not provided") -> str:
    """Record a customer issue for human support follow-up."""

    ticket_id = "TS-" + uuid4().hex[:8].upper()

    ticket = (
        f"Ticket ID: {ticket_id}\n"
        f"Created: {datetime.now().astimezone().isoformat(timespec='seconds')}\n"
        f"Order ID: {order_id}\n"
        f"Issue: {issue}\n"
        f"{'-' * 40}\n"
    )

    with open(TICKET_FILE, "a", encoding="utf-8") as file:
        file.write(ticket)

    return (
        f"Support request recorded. Ticket ID: {ticket_id}. "
        "This is a local record; a human support representative "
        "has not yet been notified."
    )
