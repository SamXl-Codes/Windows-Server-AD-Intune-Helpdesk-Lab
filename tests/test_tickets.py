import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from labtools.tickets import load_tickets, parse_timestamp, summarise, Ticket
from labtools.__main__ import render_html

SAMPLE = Path(__file__).resolve().parents[1] / 'sample-data/tickets.csv'
AS_OF = parse_timestamp('2026-11-26T12:00:00+00:00')

class TicketTests(unittest.TestCase):
    def test_load_records(self):
        self.assertEqual(len(load_tickets(SAMPLE)), 6)
    def test_summary(self):
        report = summarise(load_tickets(SAMPLE), AS_OF)
        self.assertEqual((report['total'], report['resolved'], report['open']), (6, 4, 2))
        self.assertEqual(report['breached'], 2)
    def test_expected_priorities(self):
        self.assertEqual(summarise(load_tickets(SAMPLE), AS_OF)['priorities'], {'P1':1,'P2':2,'P3':2,'P4':1})
    def test_exact_boundary_is_not_breached(self):
        ticket = Ticket('X', parse_timestamp('2026-11-26T08:00:00Z'),None,'P1','open','Test','Example')
        self.assertFalse(ticket.breached_at(parse_timestamp('2026-11-26T12:00:00Z')))
    def test_one_second_over_target(self):
        ticket = Ticket('X', parse_timestamp('2026-11-26T08:00:00Z'),None,'P1','open','Test','Example')
        self.assertTrue(ticket.breached_at(parse_timestamp('2026-11-26T12:00:01Z')))
    def test_reject_naive_timestamp(self):
        with self.assertRaises(ValueError): parse_timestamp('2026-11-26T08:00:00')
    def test_reject_future_asof(self):
        with self.assertRaises(ValueError): summarise(load_tickets(SAMPLE),parse_timestamp('2026-11-20T00:00:00Z'))
    def test_reject_resolution_before_open(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'bad.csv'
            p.write_text('ticket_id,opened_at,resolved_at,priority,status,category,summary\nX,2026-11-26T12:00:00Z,2026-11-26T11:00:00Z,P2,resolved,Test,Example\n')
            with self.assertRaises(ValueError): load_tickets(p)
    def test_reject_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'bad.csv'
            p.write_text('ticket_id,opened_at,resolved_at,priority,status,category,summary\nX,2026-11-26T10:00:00Z,,P2,open,Test,Example\nX,2026-11-26T11:00:00Z,,P2,open,Test,Example\n')
            with self.assertRaises(ValueError): load_tickets(p)
    def test_reject_inconsistent_status(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'bad.csv'
            p.write_text('ticket_id,opened_at,resolved_at,priority,status,category,summary\nX,2026-11-26T10:00:00Z,,P2,resolved,Test,Example\n')
            with self.assertRaises(ValueError): load_tickets(p)
    def test_report_html_escaped(self):
        report=summarise([Ticket('X',parse_timestamp('2026-11-26T08:00:00Z'),None,'P1','open','Test','<script>alert(1)</script>')],AS_OF)
        html=render_html(report)
        self.assertNotIn('<script>',html)
        self.assertIn('&lt;script&gt;',html)
    def test_report_has_synthetic_watermark(self):
        self.assertIn('SYNTHETIC DATA',render_html(summarise(load_tickets(SAMPLE),AS_OF)))

if __name__=='__main__':unittest.main()
