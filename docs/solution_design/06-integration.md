# Integration

[< Back to Solution Outline](README.md)

---

## Rebrickable REST API

| Property | Value |
|---|---|
| Base URL | `https://rebrickable.com/api/v3/lego/` |
| Authentication | API key via `Authorization: key {api_key}` header |
| Credentials Storage | Databricks Secrets (`scope: rebrickable`, `key: api-key`) |
| Rate Limit | ~1 request per second (enforced with 1.1s delay between requests) |
| Pagination | Cursor-based (`next` URL in response body), page size of 1000 |
| Response Format | JSON with `count`, `next`, `previous`, and `results` fields |
| Error Handling | HTTP status code validation via `raise_for_status()` |
| Timeout | 30 seconds per request |

**Endpoints consumed:**

| Endpoint | Entity | Approx. Record Count |
|---|---|---|
| `/lego/colors/` | Colors | ~200 |
| `/lego/themes/` | Themes | ~500 |
| `/lego/sets/` | Sets | ~22,000 |
| `/lego/parts/` | Parts | ~50,000 |
| `/lego/part_categories/` | Part Categories | ~70 |
| `/lego/minifigs/` | Minifigures | ~14,000 |

---

## CSV File Ingestion

Inventory-related entities are ingested from CSV files uploaded to Databricks external volumes. These files are sourced from the Rebrickable database export and loaded using PySpark's CSV reader with inferred schemas.

| File | Entity | Approx. Record Count |
|---|---|---|
| `inventories.csv` | Inventories | ~40,000 |
| `inventory_parts.csv` | Inventory Parts | ~1,100,000 |
| `inventory_minifigs.csv` | Inventory Minifigs | ~50,000 |
| `inventory_sets.csv` | Inventory Sets | ~3,000 |

---

## Power BI Integration

Power BI connects to the Gold layer tables through the **Databricks SQL Endpoint** using the Databricks connector. The dimensional model is designed to support a tabular semantic model with:

- Direct Query or Import mode against Gold layer tables
- Star schema relationships configured in the Power BI model
- Pre-aggregated fact tables reducing the need for complex DAX calculations
