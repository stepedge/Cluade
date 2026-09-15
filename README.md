# Cluade - Todo Application

A simple todo application for managing tasks.

## Features

- Add, view, and complete todos
- Persistent storage
- Simple command-line interface

## Tenders / RFQ Tracking

`tenders.py` tracks tenders and RFQs through submission, compliance, and
costing:

- Record required compliance documents (e.g. OEM letters, tax clearance)
  and flag any still missing
- Radius-based cost markup: 30-35% within 50km, 25-100% beyond, with VAT
  applied on top
- Automatic follow-up flags: 45 days after an RFQ submission, 55 days
  after a tender submission

Run `python3 tenders.py` for a demo, or `python3 test_tenders.py` to run
its tests.
