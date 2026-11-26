"""Offline ticket report CLI. Example: python -m labtools report --file sample-data/tickets.csv"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from .tickets import load_tickets, parse_timestamp, summarise


def render_html(report: dict) -> str:
    cards = [("Total tickets", report["total"]), ("Resolved", report["resolved"]),
             ("Open", report["open"]), ("Outside example target", report["breached"])]
    cells = "".join(f'<article class="stat"><small>{escape(name)}</small><strong>{value}</strong></article>' for name, value in cards)
    rows = "".join(
        f'<tr><td>{escape(t["ticket_id"])}</td><td>{escape(t["summary"])}</td>'
        f'<td>{escape(t["category"])}</td><td>{escape(t["priority"])}</td>'
        f'<td><span class="pill">{escape(t["status"].title())}</span></td>'
        f'<td class="{"bad" if t["breached"] else "good"}">{"Outside target" if t["breached"] else "Within target"}</td></tr>'
        for t in report["rows"]
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline Help Desk Demo</title>
<style>
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{margin:0;background:#f6f7f9;color:#171e2c;font:15px system-ui,-apple-system,Segoe UI,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:38px 44px 48px}}.top{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}}
.eyebrow{{font-size:12px;font-weight:750;letter-spacing:1.5px;color:#536174;text-transform:uppercase}}h1{{font-size:34px;letter-spacing:-1px;margin:8px 0 10px}}p{{color:#5b6779;margin:0;line-height:1.5}}.sample{{background:#fff1d7;border:1px solid #f0d39d;padding:12px 16px;border-radius:9px;color:#754800;font-size:13px;font-weight:750;white-space:nowrap}}.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:34px 0}}
.stat{{background:white;border:1px solid #e3e7ee;border-radius:13px;padding:22px;box-shadow:0 3px 10px #1c2f5210}}.stat small{{font-weight:600;color:#667084}}.stat strong{{display:block;margin-top:12px;font-size:38px;letter-spacing:-1.3px}}.card{{border:1px solid #e2e6ed;background:#fff;border-radius:13px;overflow:hidden;box-shadow:0 3px 10px #1c2f520a}}.card header{{padding:22px 26px;border-bottom:1px solid #e8ebf0;font-weight:750;font-size:17px}}table{{border-collapse:collapse;width:100%}}th{{text-align:left;background:#f9fafc;color:#607083;font-size:12px;letter-spacing:.3px;padding:15px 20px}}td{{border-top:1px solid #e8ebf0;padding:17px 20px;font-size:13px}}.pill{{display:inline-block;background:#f0f3f8;padding:6px 10px;border-radius:16px;text-transform:capitalize}}.bad{{color:#a64d32;font-weight:700}}.good{{color:#2b7160;font-weight:700}}footer{{margin-top:18px;color:#607083;font-size:12px}}</style></head><body>
<main class="wrap"><div class="top"><div><div class="eyebrow">IT operations / offline report</div><h1>Help desk ticket overview</h1><p>Illustrative resolution targets · As of {escape(report['as_of'])}</p></div><div class="sample">SYNTHETIC DATA · DEMO ONLY</div></div>
<section class="stats">{cells}</section><section class="card"><header>Ticket activity</header><table><thead><tr><th>ID</th><th>Summary</th><th>Category</th><th>Priority</th><th>Status</th><th>Example SLA</th></tr></thead><tbody>{rows}</tbody></table></section>
<footer>Fictional ticket records. Not connected to osTicket, Active Directory, Intune or a company service desk. Targets use elapsed clock hours and omit business calendars.</footer></main></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic help-desk CSV analyzer")
    parser.add_argument("command", choices=["report"])
    parser.add_argument("--file", required=True, help="CSV with fictional tickets")
    parser.add_argument("--as-of", default=None, help="ISO timestamp; default current UTC")
    parser.add_argument("--html", help="Write synthetic HTML demo report to this path")
    args = parser.parse_args()
    as_of = parse_timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
    report = summarise(load_tickets(args.file), as_of)
    print("SYNTHETIC HELP DESK DEMO - NOT LIVE OSTICKET DATA")
    print(f"As of: {report['as_of']}")
    print(f"Tickets: {report['total']}  Resolved: {report['resolved']}  Open: {report['open']}")
    print(f"Within example target: {report['within_target']}  Outside target: {report['breached']}")
    for row in report['rows']:
        print(f"  {row['ticket_id']:9} {row['priority']:3} {row['status']:8} {'BREACHED' if row['breached'] else 'WITHIN':8} {row['summary']}")
    if args.html:
        path = Path(args.html)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_html(report), encoding="utf-8")
        print(f"Report: {path}")


if __name__ == "__main__":
    main()
