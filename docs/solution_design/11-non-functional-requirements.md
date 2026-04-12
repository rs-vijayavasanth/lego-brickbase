# Non-Functional Requirements

[< Back to Solution Outline](README.md)

---

## Performance

| Consideration | Approach |
|---|---|
| API Rate Limiting | 1.1-second delay between API requests to stay within the ~1 req/sec limit |
| Partitioning | Silver tables partitioned by `valid_from_date` for efficient time-based queries |
| Pre-aggregation | Gold fact tables (`fct_set_composition`, `fct_color_usage`, `fct_part_usage`, `fct_theme_summary`) pre-aggregate metrics to reduce query-time computation |
| Single-file Writes | Bronze Parquet writes coalesced to a single file per load to avoid small file overhead |
| Delta Optimisation | Delta Lake format enables data skipping, Z-ordering, and OPTIMIZE operations |

---

## Scalability

| Consideration | Approach |
|---|---|
| Data Volume | Current dataset is moderate (~1.2M inventory part records). PySpark and Delta Lake are designed to scale to much larger volumes without architecture changes. |
| API Pagination | Page size of 1,000 records with automatic cursor-based pagination handles growing datasets |
| Notebook Modularity | Each entity is processed by an independent notebook, enabling horizontal scaling of execution |

---

## Reliability

| Consideration | Approach |
|---|---|
| Idempotency | All notebooks are idempotent - safe to re-run without duplicating data |
| Error Handling | HTTP requests use `raise_for_status()` with 30-second timeouts |
| Delta ACID | Delta Lake MERGE operations are atomic - partial failures do not corrupt table state |
| SCD2 Resilience | Soft deletes and version tracking ensure no data loss even when source records are removed |

---

## Maintainability

| Consideration | Approach |
|---|---|
| Documentation | Every notebook contains markdown cells explaining its purpose, steps, and configuration |
| Standardised Patterns | Bronze, Silver, and Gold notebooks each follow a consistent repeatable pattern |
| Separation of Concerns | Each layer has a distinct responsibility; each entity has its own notebook |
| Changelog | Version-controlled changelog tracks all changes and breaking modifications |
