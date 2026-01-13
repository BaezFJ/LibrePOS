# Auth Blueprint Schema

> Authentication, sessions, and API keys (3 tables)

---

## login_attempt

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NULL | Null if unknown user |
| attempt_time | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| success | BOOLEAN | NOT NULL | |
| ip_address | VARCHAR(45) | NOT NULL | IPv4/IPv6 |
| user_agent | TEXT | | |

---

## active_session

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| session_token | VARCHAR(255) | NOT NULL, UNIQUE | |
| device_info | VARCHAR(255) | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| expires_at | TIMESTAMPTZ | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## api_key

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| key_hash | VARCHAR(255) | NOT NULL, UNIQUE | Never store plain |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| scopes | JSONB | NOT NULL, DEFAULT '[]' | Permitted API scopes |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| expires_at | TIMESTAMPTZ | | Optional |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| last_used_at | TIMESTAMPTZ | | |
