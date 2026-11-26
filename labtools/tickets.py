"""CSV ticket/SLA demonstration. Uses fictional data and elapsed clock-hour targets."""
from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

SLA_HOURS = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
REQUIRED = {"ticket_id", "opened_at", "resolved_at", "priority", "status", "category", "summary"}


def parse_timestamp(value: str) -> datetime:
    if not value.strip():
        raise ValueError("Timestamp must be provided")
    instant = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError(f"Timezone required: {value}")
    return instant.astimezone(timezone.utc)


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    opened_at: datetime
    resolved_at: datetime | None
    priority: str
    status: str
    category: str
    summary: str

    def due_at(self) -> datetime:
        return self.opened_at + timedelta(hours=SLA_HOURS[self.priority])

    def breached_at(self, as_of: datetime) -> bool:
        comparison = self.resolved_at or as_of
        return comparison > self.due_at()


def load_tickets(path: str | Path) -> list[Ticket]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"Missing required columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        rows = list(reader)
    result: list[Ticket] = []
    identifiers = set()
    for row in rows:
        key = (row["ticket_id"] or "").strip()
        if not key or key in identifiers:
            raise ValueError(f"Missing or duplicate ticket id: {key!r}")
        identifiers.add(key)
        priority = row["priority"].strip().upper()
        if priority not in SLA_HOURS:
            raise ValueError(f"Invalid priority in {key}: {priority}")
        opened = parse_timestamp(row["opened_at"])
        resolved = parse_timestamp(row["resolved_at"]) if row["resolved_at"].strip() else None
        if resolved and resolved < opened:
            raise ValueError(f"Resolved before opened: {key}")
        status = row["status"].strip().lower()
        if status not in {"open", "resolved"}:
            raise ValueError(f"Invalid status in {key}: {status}")
        if (status == "resolved") != (resolved is not None):
            raise ValueError(f"Inconsistent resolution timestamp/status: {key}")
        result.append(Ticket(key, opened, resolved, priority, status,
                             row["category"].strip(), row["summary"].strip()))
    return result


def summarise(tickets: list[Ticket], as_of: datetime) -> dict:
    if as_of.tzinfo is None:
        raise ValueError("as_of needs a timezone")
    as_of = as_of.astimezone(timezone.utc)
    categories = Counter(t.category for t in tickets)
    priorities = Counter(t.priority for t in tickets)
    open_tickets = [t for t in tickets if t.status == "open"]
    resolved_tickets = [t for t in tickets if t.status == "resolved"]
    eligible = [t for t in tickets if t.opened_at <= as_of]
    if len(eligible) != len(tickets):
        raise ValueError("as_of precedes the opening of one or more tickets")
    if any(t.resolved_at and t.resolved_at > as_of for t in tickets):
        raise ValueError("as_of precedes a completed resolution")
    breached = [t for t in tickets if t.breached_at(as_of)]
    return {
        "as_of": as_of.isoformat(), "total": len(tickets),
        "open": len(open_tickets), "resolved": len(resolved_tickets),
        "breached": len(breached), "within_target": len(tickets) - len(breached),
        "categories": dict(sorted(categories.items())),
        "priorities": dict(sorted(priorities.items())),
        "rows": [{"ticket_id": t.ticket_id, "priority": t.priority, "category": t.category,
                  "status": t.status, "opened_at": t.opened_at.isoformat(),
                  "due_at": t.due_at().isoformat(),
                  "breached": t.breached_at(as_of), "summary": t.summary}
                 for t in tickets],
        "note": "SYNTHETIC LAB DATA. Elapsed clock-hour example targets, not osTicket live data or contractual SLAs."
    }
