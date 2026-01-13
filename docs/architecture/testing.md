# Testing Structure

> Test organization, fixtures, and running tests.

---

## Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py                   # Shared fixtures
│   ├── app fixture               # Test app instance
│   ├── client fixture            # Test client
│   ├── db fixture                # Test database
│   └── auth fixtures             # Logged-in user states
│
├── unit/                         # Unit tests (isolated)
│   ├── test_menu/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_schemas.py
│   ├── test_orders/
│   ├── test_payments/
│   └── ...
│
├── integration/                  # Integration tests
│   ├── test_order_flow.py        # Order → Payment flow
│   ├── test_kitchen_routing.py   # Order → Kitchen tickets
│   └── test_inventory_deduct.py  # Sale → Stock adjustment
│
└── e2e/                          # End-to-end tests
    ├── test_complete_sale.py     # Full customer journey
    └── test_shift_workflow.py    # Clock in → Sales → Clock out
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run specific blueprint tests
pytest tests/unit/test_orders/

# Run with coverage
pytest --cov=app --cov-report=html

# Run integration tests only
pytest tests/integration/
```
