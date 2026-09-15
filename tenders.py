#!/usr/bin/env python3
"""Tender / RFQ tracking module.

Tracks tenders and RFQs through submission, compliance checks,
costing, and pipeline follow-up alerts.
"""

import json
import os
from datetime import date, datetime, timedelta

RFQ_FOLLOW_UP_DAYS = 45
TENDER_FOLLOW_UP_DAYS = 55
LOCAL_RADIUS_KM = 50
LOCAL_MARKUP_RANGE = (0.30, 0.35)
REMOTE_MARKUP_RANGE = (0.25, 1.00)
VAT_RATE = 0.15


class TenderApp:
    def __init__(self, filename="tenders.json"):
        self.filename = filename
        self.tenders = self.load_tenders()

    def load_tenders(self):
        """Load tenders from file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_tenders(self):
        """Save tenders to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.tenders, f, indent=2)

    def add_tender(self, client, title, kind="rfq", submitted_on=None,
                   required_docs=None):
        """Add a new tender or RFQ record.

        kind is "rfq" or "tender", used to pick the correct follow-up window.
        """
        tender = {
            "id": len(self.tenders) + 1,
            "client": client,
            "title": title,
            "kind": kind,
            "submitted_on": submitted_on,
            "required_docs": required_docs or [],
            "received_docs": [],
            "followed_up": False,
        }
        self.tenders.append(tender)
        self.save_tenders()
        return tender

    def list_tenders(self):
        """List all tenders."""
        return self.tenders

    def get_tender(self, tender_id):
        for tender in self.tenders:
            if tender["id"] == tender_id:
                return tender
        return None

    def mark_submitted(self, tender_id, submitted_on=None):
        """Record the submission date for a tender."""
        tender = self.get_tender(tender_id)
        if tender is None:
            return None
        tender["submitted_on"] = submitted_on or date.today().isoformat()
        self.save_tenders()
        return tender

    def record_received_docs(self, tender_id, docs):
        """Record which compliance documents have been received."""
        tender = self.get_tender(tender_id)
        if tender is None:
            return None
        for doc in docs:
            if doc not in tender["received_docs"]:
                tender["received_docs"].append(doc)
        self.save_tenders()
        return tender

    def compliance_check(self, tender_id):
        """Return required docs still missing for a tender."""
        tender = self.get_tender(tender_id)
        if tender is None:
            return None
        missing = [d for d in tender["required_docs"]
                   if d not in tender["received_docs"]]
        return {
            "tender_id": tender_id,
            "missing": missing,
            "compliant": len(missing) == 0,
        }

    def _follow_up_window(self, kind):
        return TENDER_FOLLOW_UP_DAYS if kind == "tender" else RFQ_FOLLOW_UP_DAYS

    def check_follow_ups(self, today=None):
        """Return tenders due a follow-up: 45 days (RFQ) / 55 days (tender)
        after submission."""
        today = today or date.today()
        due = []
        for tender in self.tenders:
            if not tender["submitted_on"] or tender["followed_up"]:
                continue
            submitted = datetime.fromisoformat(tender["submitted_on"]).date()
            window = self._follow_up_window(tender["kind"])
            if today >= submitted + timedelta(days=window):
                due.append(tender)
        return due

    def mark_followed_up(self, tender_id):
        tender = self.get_tender(tender_id)
        if tender is None:
            return None
        tender["followed_up"] = True
        self.save_tenders()
        return tender

    def calculate_costing(self, cost_ex_vat, delivery_km, markup=None):
        """Apply radius-based markup and VAT to a cost.

        Within LOCAL_RADIUS_KM: markup must fall in LOCAL_MARKUP_RANGE.
        Beyond it: markup must fall in REMOTE_MARKUP_RANGE.
        If markup is not given, the lower bound of the applicable range is used.
        """
        is_local = delivery_km <= LOCAL_RADIUS_KM
        low, high = LOCAL_MARKUP_RANGE if is_local else REMOTE_MARKUP_RANGE

        if markup is None:
            markup = low
        elif not (low <= markup <= high):
            raise ValueError(
                f"markup {markup:.0%} out of range "
                f"({low:.0%}-{high:.0%}) for delivery_km={delivery_km}"
            )

        subtotal = cost_ex_vat * (1 + markup)
        total_inc_vat = subtotal * (1 + VAT_RATE)
        return {
            "cost_ex_vat": cost_ex_vat,
            "delivery_km": delivery_km,
            "is_local": is_local,
            "markup": markup,
            "subtotal": round(subtotal, 2),
            "total_inc_vat": round(total_inc_vat, 2),
        }


def main():
    app = TenderApp()

    t1 = app.add_tender(
        "Acme Corp", "Office network refresh RFQ", kind="rfq",
        required_docs=["OEM Letter", "Tax Clearance"],
    )
    app.mark_submitted(t1["id"], "2026-06-01")
    app.record_received_docs(t1["id"], ["OEM Letter"])

    print("Tenders:")
    for tender in app.list_tenders():
        print(f"  [{tender['id']}] {tender['client']} - {tender['title']}"
              f" ({tender['kind']})")

    print("\nCompliance check:", app.compliance_check(t1["id"]))

    print("\nFollow-ups due today:")
    for tender in app.check_follow_ups():
        print(f"  [{tender['id']}] {tender['client']} - {tender['title']}")

    print("\nCosting example (local delivery):")
    print(app.calculate_costing(10000, delivery_km=20, markup=0.32))

    print("\nCosting example (remote delivery):")
    print(app.calculate_costing(10000, delivery_km=300, markup=0.50))


if __name__ == "__main__":
    main()
