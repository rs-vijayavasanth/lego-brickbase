# Governance and Compliance

[< Back to Solution Outline](README.md)

---

## Data Quality

| Practice | Implementation |
|---|---|
| Schema Enforcement | Explicit schemas defined in Bronze ingestion notebooks; Delta Lake rejects schema-violating writes |
| SCD2 History | Full change history preserved in Bronze, enabling point-in-time audit |
| Soft Deletes | Records removed from the source are flagged (`is_deleted = true`) rather than physically deleted |
| Constraint Documentation | Primary keys and foreign keys declared on all Gold tables |
| Column Documentation | Every Gold table column has a `COMMENT` describing its business meaning |
| Table Documentation | Every Gold table has a table-level `COMMENT` describing its grain and purpose |

---

## Data Lineage

Data lineage is traceable through:

1. **Audit columns** (`_load_datetime`, `_record_source`) - Track when and from where each record was ingested
2. **SCD2 metadata** (`valid_from`, `valid_to`) - Track the temporal validity of each record version
3. **Unity Catalog lineage** - Automatic column-level lineage tracking through Spark operations
4. **Notebook documentation** - Each notebook contains markdown cells describing its inputs, transformations, and outputs

---

## Change Management

| Practice | Implementation |
|---|---|
| Version Control | All notebooks and documentation stored in Git (GitHub) |
| Pull Request Reviews | Changes require PR review using the project's validation checklist |
| Changelog | [CHANGELOG.md](../../CHANGELOG.md) tracks all notable changes per [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) |
| Breaking Change Tracking | Breaking changes (table/column renames, datatype changes) are explicitly flagged in the changelog |

---

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Catalog | Lowercase, underscore-separated | `lego_brickbase` |
| Schema | Layer name | `bronze`, `silver`, `gold` |
| Bronze Tables | `raw_{entity}` | `raw_sets`, `raw_colors` |
| Silver Tables | `foundation_{entity}` | `foundation_sets` |
| Dimension Tables | `dim_{entity}` | `dim_set`, `dim_color` |
| Fact Tables | `fct_{entity}` (singular) | `fct_set_inventory` |
| Surrogate Keys | `{entity}_key` | `set_key`, `color_key` |
| Foreign Keys | `{referenced_entity}_key` | `theme_key` in `dim_set` |
| Audit Columns | Prefixed with `_` | `_load_datetime`, `_record_source` |
