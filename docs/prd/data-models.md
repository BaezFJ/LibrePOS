# Data Models by Blueprint

> Complete model definitions for all blueprints

---

## Auth Blueprint

| Model | Key Fields |
|-------|------------|
| LoginAttempt | id, user_id, attempt_time, success, ip_address, user_agent |
| ActiveSession | id, user_id, session_token, device_info, created_at, expires_at, is_active |
| APIKey | id, name, key_hash, user_id, scopes, created_at, expires_at, is_active, last_used_at |

---

## Menu Blueprint

| Model | Key Fields |
|-------|------------|
| Category | id, name, description, display_order, parent_id, is_active, image_url |
| MenuItem | id, name, description, price, category_id, sku, is_available, is_taxable, prep_time_minutes |
| ModifierGroup | id, name, min_selections, max_selections, is_required, display_order |
| Modifier | id, name, price, modifier_group_id, is_available, display_order |
| Combo | id, name, description, price, is_active, start_date, end_date |
| PricingRule | id, menu_item_id, rule_type, price, start_time, end_time, days_of_week, priority |
| MenuSchedule | id, name, menu_items (M2M), start_date, end_date, days_of_week, start_time, end_time |

---

## Orders Blueprint

| Model | Key Fields |
|-------|------------|
| Order | id, order_number, order_type, status, table_id, server_id, customer_id, guest_count, notes, created_at |
| OrderItem | id, order_id, menu_item_id, quantity, unit_price, notes, course, seat_number, status, void_reason |
| OrderItemModifier | id, order_item_id, modifier_id, quantity, unit_price |
| Check | id, order_id, check_number, subtotal, tax_amount, discount_amount, total, status, created_at |
| CheckItem | id, check_id, order_item_id |

---

## Payments Blueprint

| Model | Key Fields |
|-------|------------|
| Payment | id, check_id, amount, tender_type, status, reference_number, processor_response, created_at |
| Tip | id, payment_id, amount, entry_method, declared_by_id, created_at, adjusted_at |
| Discount | id, name, discount_type, value, code, requires_authorization, is_active, usage_limit |
| TaxRate | id, name, rate, jurisdiction, applies_to, is_inclusive, is_active |
| CashDrawer | id, name, station_id, status, opened_at, opened_by_id, opening_amount, current_amount |
| Receipt | id, payment_id, receipt_type, delivery_method, content, delivered_at, email, phone |

---

## Staff Blueprint

| Model | Key Fields |
|-------|------------|
| User | id, employee_number, first_name, last_name, email, phone, pin_hash, password_hash, role_id, is_active |
| Role | id, name, description, is_system_role, created_at |
| Permission | id, code, name, description, category |
| RolePermission | id, role_id, permission_id |
| TimeEntry | id, user_id, clock_in, clock_out, break_minutes, shift_id, is_edited, edit_reason |
| Shift | id, user_id, scheduled_start, scheduled_end, actual_start, actual_end, role_id, notes |
| TipDeclaration | id, user_id, shift_date, cash_tips, credit_tips, tip_out_given, tip_out_received |

---

## Kitchen Blueprint

| Model | Key Fields |
|-------|------------|
| Station | id, name, station_type, display_order, is_active, printer_id |
| CategoryStation | id, category_id, station_id |
| KitchenTicket | id, order_id, station_id, status, priority, created_at, started_at, completed_at, bumped_at |
| KitchenTicketItem | id, ticket_id, order_item_id, quantity, notes, status, position |
| KitchenMessage | id, from_user_id, to_station_id, message, is_read, created_at |
| PrepTime | id, menu_item_id, station_id, average_seconds, sample_count, last_updated |

---

## Tables Blueprint

| Model | Key Fields |
|-------|------------|
| FloorPlan | id, name, is_active, is_default, created_at |
| Table | id, floor_plan_id, table_number, name, capacity_min, capacity_max, x_position, y_position, shape |
| Section | id, floor_plan_id, name, color, created_at |
| TableStatus | id, table_id, status, party_size, server_id, order_id, seated_at, status_changed_at |
| Reservation | id, customer_name, phone, email, party_size, reservation_time, table_id, status, notes, source |
| WaitlistEntry | id, customer_name, phone, party_size, quoted_wait_minutes, check_in_time, status, notes |

---

## Reporting Blueprint

| Model | Key Fields |
|-------|------------|
| DailySummary | id, business_date, gross_sales, net_sales, tax_collected, discounts_given, refunds, tips_collected |
| HourlySales | id, business_date, hour, sales_amount, order_count, guest_count |
| SavedReport | id, name, report_type, parameters, created_by_id, is_scheduled, schedule_cron, email_recipients |
| AuditLog | id, user_id, action, entity_type, entity_id, old_values, new_values, ip_address, created_at |

---

## Inventory Blueprint

| Model | Key Fields |
|-------|------------|
| InventoryItem | id, name, sku, category, unit_of_measure, unit_cost, par_level, reorder_point, is_active |
| StockLevel | id, inventory_item_id, storage_location, quantity_on_hand, last_counted_at, last_updated_at |
| Recipe | id, menu_item_id, yield_quantity, yield_unit, instructions, is_active |
| RecipeIngredient | id, recipe_id, inventory_item_id, quantity, unit, waste_factor_percent |
| Vendor | id, name, contact_name, email, phone, address, payment_terms, lead_time_days, is_active |
| PurchaseOrder | id, po_number, vendor_id, status, order_date, expected_date, subtotal, tax, total, created_by_id |
| POLineItem | id, purchase_order_id, inventory_item_id, quantity_ordered, unit_cost, quantity_received |

---

## Customers Blueprint

| Model | Key Fields |
|-------|------------|
| Customer | id, first_name, last_name, email, phone, marketing_opt_in, birthday, notes, tags, source |
| CustomerPreference | id, customer_id, preference_type, preference_value, notes |
| LoyaltyAccount | id, customer_id, tier_id, points_balance, lifetime_points, points_expiring, enrolled_at |
| LoyaltyTransaction | id, loyalty_account_id, transaction_type, points, order_id, description, created_at |
| Reward | id, name, description, points_required, reward_type, reward_value, menu_item_id, is_active |
| GiftCard | id, card_number, pin_hash, initial_balance, current_balance, status, issued_at, expires_at |
| Feedback | id, customer_id, order_id, rating, food_rating, service_rating, comment, response, created_at |

---

## Integrations Blueprint

| Model | Key Fields |
|-------|------------|
| Integration | id, name, integration_type, provider, is_active, config, credentials, last_sync_at |
| WebhookEndpoint | id, integration_id, url, secret_hash, events, is_active, created_at |
| WebhookLog | id, endpoint_id, event_type, payload, response_status, response_body, sent_at, retry_count |
| ExternalOrder | id, integration_id, external_id, order_id, status, external_status, raw_data, received_at |
| SyncLog | id, integration_id, sync_type, direction, status, records_processed, errors, started_at |
