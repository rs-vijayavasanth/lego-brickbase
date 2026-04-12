# Data Pipeline

[< Back to Solution Outline](README.md)

---

## Pipeline Stages

The pipeline executes in strict layer order with dependencies between layers:

```mermaid
graph LR
    A["Bronze (10 notebooks)"] -->  B["Silver (10 notebooks)"] --> C["Gold (14 notebooks)"]
```

Each notebook is **idempotent** - it can be re-executed safely without producing duplicate data:

- Bronze uses SCD2 merge (MERGE INTO with matched update and insert)
- Silver uses `CREATE OR REPLACE TABLE`
- Gold uses `overwrite` mode write followed by `CREATE OR REPLACE TABLE`

---

## Bronze Ingestion Pattern

Every Bronze notebook follows this standardised pattern:

1. **Fetch** - Retrieve all records from API (paginated) or CSV
2. **Convert** - Map to a typed Spark DataFrame with an explicit schema
3. **Write Raw** - Append audit columns and write Parquet to a date/time-partitioned path under the external volume
4. **SCD2 Merge** - Merge into the Delta table:
   - *First load:* Write all records as current
   - *Subsequent loads:* Expire changed records, soft-delete removed records, insert new/changed records
5. **Register** - Create the Unity Catalog table if it does not exist

---

## Silver Transformation Pattern

Every Silver notebook follows this standardised pattern:

1. **Read** - Load the Bronze Delta table, filtering to `is_current = true` and `is_deleted = false`
2. **Transform** - Rename natural keys to `{entity}_key` convention, alias columns to business-friendly names
3. **Write** - Overwrite the Delta table with `CREATE OR REPLACE TABLE`, partitioned by `valid_from_date`
4. **Register** - Table is automatically registered via the `CREATE OR REPLACE` statement

---

## Gold Modeling Pattern

Every Gold notebook follows this standardised pattern:

1. **Read** - Load required Silver foundation tables and/or other Gold tables
2. **Transform** - Join, aggregate, enrich, and derive calculated columns
3. **Write** - Overwrite the Delta volume path
4. **Register** - `CREATE OR REPLACE TABLE` with full DDL including column types, NOT NULL constraints, comments, and table-level descriptions
5. **Constrain** - Apply PRIMARY KEY, FOREIGN KEY, and PARENT KEY constraints
6. **Load** - `INSERT INTO` from the Delta volume path

---

## Execution Dependencies

```
Bronze Layer (independent - can run in parallel):
  load_colors, load_themes, load_sets, load_parts,
  load_part_categories, load_minifigs, load_inventories,
  load_inventory_parts, load_inventory_minifigs, load_inventory_sets

Silver Layer (independent - can run in parallel after Bronze):
  foundation_colors, foundation_themes, foundation_sets, foundation_parts,
  foundation_part_categories, foundation_minifigs, foundation_inventories,
  foundation_inventory_parts, foundation_inventory_minifigs, foundation_inventory_sets

Gold Layer (ordered dependencies):
  1. dim_theme_hierarchy  (depends on: foundation_themes)
  2. dim_color            (depends on: foundation_colors)
  3. dim_part             (depends on: foundation_parts, foundation_part_categories)
  4. dim_set              (depends on: foundation_sets, dim_theme_hierarchy,
                           foundation_inventories, foundation_inventory_parts,
                           foundation_inventory_minifigs)
  5. fct_set_inventory    (depends on: dim_set, dim_part, dim_color,
                           foundation_inventories, foundation_inventory_parts)
  6. fct_set_minifigs     (depends on: dim_set, foundation_inventories,
                           foundation_inventory_minifigs, foundation_minifigs)
  7. fct_set_composition  (depends on: fct_set_inventory, fct_set_minifigs)
  8. fct_color_usage      (depends on: fct_set_inventory, dim_color)
  9. fct_part_usage       (depends on: fct_set_inventory, dim_part)
  10. fct_theme_summary   (depends on: dim_set, fct_set_inventory, fct_set_minifigs)
```
