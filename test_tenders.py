#!/usr/bin/env python3
"""Tests for the tender/RFQ tracking module."""

import os
import tempfile
from datetime import date, timedelta

from tenders import TenderApp


def make_app(tmpdir):
    return TenderApp(os.path.join(tmpdir, "test_tenders.json"))


def test_add_and_list_tender():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        tender = app.add_tender("Acme Corp", "Network refresh", kind="rfq")
        assert tender["id"] == 1
        assert len(app.list_tenders()) == 1
        print("✓ add_and_list_tender test passed")


def test_compliance_check_flags_missing_docs():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        tender = app.add_tender(
            "Acme Corp", "Network refresh", kind="rfq",
            required_docs=["OEM Letter", "Tax Clearance"],
        )
        result = app.compliance_check(tender["id"])
        assert result["compliant"] is False
        assert set(result["missing"]) == {"OEM Letter", "Tax Clearance"}

        app.record_received_docs(tender["id"], ["OEM Letter", "Tax Clearance"])
        result = app.compliance_check(tender["id"])
        assert result["compliant"] is True
        assert result["missing"] == []
        print("✓ compliance_check_flags_missing_docs test passed")


def test_rfq_follow_up_after_45_days():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        tender = app.add_tender("Acme Corp", "RFQ", kind="rfq")
        submitted = date(2026, 1, 1)
        app.mark_submitted(tender["id"], submitted.isoformat())

        assert app.check_follow_ups(today=submitted + timedelta(days=44)) == []
        due = app.check_follow_ups(today=submitted + timedelta(days=45))
        assert len(due) == 1 and due[0]["id"] == tender["id"]
        print("✓ rfq_follow_up_after_45_days test passed")


def test_tender_follow_up_after_55_days():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        tender = app.add_tender("Acme Corp", "Tender", kind="tender")
        submitted = date(2026, 1, 1)
        app.mark_submitted(tender["id"], submitted.isoformat())

        assert app.check_follow_ups(today=submitted + timedelta(days=54)) == []
        due = app.check_follow_ups(today=submitted + timedelta(days=55))
        assert len(due) == 1 and due[0]["id"] == tender["id"]
        print("✓ tender_follow_up_after_55_days test passed")


def test_follow_up_skipped_once_marked_done():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        tender = app.add_tender("Acme Corp", "RFQ", kind="rfq")
        submitted = date(2026, 1, 1)
        app.mark_submitted(tender["id"], submitted.isoformat())
        app.mark_followed_up(tender["id"])

        due = app.check_follow_ups(today=submitted + timedelta(days=60))
        assert due == []
        print("✓ follow_up_skipped_once_marked_done test passed")


def test_costing_local_delivery_within_range():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        result = app.calculate_costing(1000, delivery_km=10, markup=0.30)
        assert result["is_local"] is True
        assert result["subtotal"] == 1300.0
        assert result["total_inc_vat"] == 1495.0
        print("✓ costing_local_delivery_within_range test passed")


def test_costing_remote_delivery_within_range():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        result = app.calculate_costing(1000, delivery_km=200, markup=0.50)
        assert result["is_local"] is False
        assert result["subtotal"] == 1500.0
        assert result["total_inc_vat"] == 1725.0
        print("✓ costing_remote_delivery_within_range test passed")


def test_costing_rejects_out_of_range_markup():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)

        for delivery_km, markup in [(10, 0.50), (200, 0.10)]:
            try:
                app.calculate_costing(1000, delivery_km=delivery_km, markup=markup)
                raise AssertionError("expected ValueError for out-of-range markup")
            except ValueError:
                pass
        print("✓ costing_rejects_out_of_range_markup test passed")


def test_costing_defaults_to_lower_bound():
    with tempfile.TemporaryDirectory() as tmpdir:
        app = make_app(tmpdir)
        result = app.calculate_costing(1000, delivery_km=10)
        assert result["markup"] == 0.30
        print("✓ costing_defaults_to_lower_bound test passed")


if __name__ == "__main__":
    test_add_and_list_tender()
    test_compliance_check_flags_missing_docs()
    test_rfq_follow_up_after_45_days()
    test_tender_follow_up_after_55_days()
    test_follow_up_skipped_once_marked_done()
    test_costing_local_delivery_within_range()
    test_costing_remote_delivery_within_range()
    test_costing_rejects_out_of_range_markup()
    test_costing_defaults_to_lower_bound()
    print("\nAll tests passed!")
