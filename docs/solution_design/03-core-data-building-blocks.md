# Core Data Building Blocks

[< Back to Solution Outline](README.md)

---

## Source Entities

The project ingests **10 source entities** from Rebrickable, split across two ingestion methods:

### API-Sourced Entities

| Entity | API Endpoint | Natural Key | Description |
|---|---|---|---|
| Colors | `/lego/colors/` | `id` | LEGO colour catalogue with RGB values |
| Themes | `/lego/themes/` | `id` | Hierarchical theme classification |
| Sets | `/lego/sets/` | `set_num` | Official LEGO set catalogue |
| Parts | `/lego/parts/` | `part_num` | Individual brick/element catalogue |
| Part Categories | `/lego/part_categories/` | `id` | Part classification groups |
| Minifigs | `/lego/minifigs/` | `set_num` | Minifigure catalogue |

### CSV-Sourced Entities

| Entity | File | Natural Key | Description |
|---|---|---|---|
| Inventories | `inventories.csv` | `id` | Bill-of-materials header linking sets to contents |
| Inventory Parts | `inventory_parts.csv` | `inventory_id` + `part_num` + `color_id` | Part-colour-quantity per inventory |
| Inventory Minifigs | `inventory_minifigs.csv` | `inventory_id` + `fig_num` | Minifigure-quantity per inventory |
| Inventory Sets | `inventory_sets.csv` | `inventory_id` + `set_num` | Sub-set references per inventory |

---

## Bronze Layer - Raw Tables

Each source entity maps to a Bronze Delta table with the following standardised audit and SCD2 columns:

| Column | Type | Purpose |
|---|---|---|
| `_load_datetime` | `TIMESTAMP` | When the record was ingested |
| `_record_source` | `STRING` | Origin of the record (`API` or `CSV`) |
| `valid_from` | `TIMESTAMP` | When this version of the record became current |
| `valid_to` | `TIMESTAMP` | When this version was superseded (NULL if current) |
| `is_current` | `BOOLEAN` | Whether this is the latest version |
| `is_deleted` | `BOOLEAN` | Whether the record was soft-deleted from source |

**Bronze Tables:**

| Catalog Table | Natural Key |
|---|---|
| `lego_brickbase.bronze.raw_colors` | `id` |
| `lego_brickbase.bronze.raw_themes` | `id` |
| `lego_brickbase.bronze.raw_sets` | `set_num` |
| `lego_brickbase.bronze.raw_parts` | `part_num` |
| `lego_brickbase.bronze.raw_part_categories` | `id` |
| `lego_brickbase.bronze.raw_minifigs` | `set_num` |
| `lego_brickbase.bronze.raw_inventories` | `id` |
| `lego_brickbase.bronze.raw_inventory_parts` | `inventory_id` + `part_num` + `color_id` |
| `lego_brickbase.bronze.raw_inventory_minifigs` | `inventory_id` + `fig_num` |
| `lego_brickbase.bronze.raw_inventory_sets` | `inventory_id` + `set_num` |

---

## Silver Layer - Foundation Tables

Foundation tables apply the following standardisations to Bronze data:

- **Filter** to `is_current = true` and `is_deleted = false` records only
- **Rename** natural keys to a consistent `{entity}_key` convention (e.g., `set_num` becomes `set_key`)
- **Alias** columns to business-friendly names
- **Partition** by `valid_from_date` for query performance

**Silver Tables:**

| Catalog Table | Surrogate Key | Source Bronze Table |
|---|---|---|
| `lego_brickbase.silver.foundation_colors` | `color_key` | `raw_colors` |
| `lego_brickbase.silver.foundation_themes` | `theme_key` | `raw_themes` |
| `lego_brickbase.silver.foundation_sets` | `set_key` | `raw_sets` |
| `lego_brickbase.silver.foundation_parts` | `part_key` | `raw_parts` |
| `lego_brickbase.silver.foundation_part_categories` | `part_category_key` | `raw_part_categories` |
| `lego_brickbase.silver.foundation_minifigs` | `minifig_key` | `raw_minifigs` |
| `lego_brickbase.silver.foundation_inventories` | `inventory_id` | `raw_inventories` |
| `lego_brickbase.silver.foundation_inventory_parts` | `inventory_id` + `part_key` + `color_key` | `raw_inventory_parts` |
| `lego_brickbase.silver.foundation_inventory_minifigs` | `inventory_id` + `minifig_key` | `raw_inventory_minifigs` |
| `lego_brickbase.silver.foundation_inventory_sets` | `inventory_id` + `set_key` | `raw_inventory_sets` |

---

## Gold Layer - Dimensional Model

The Gold layer implements a **star schema** with 4 dimension tables and 6 fact tables. See [Logical Data Model](04-logical-data-model.md) for the full schema.

### Dimensions

| Table | Grain | Key | Description |
|---|---|---|---|
| `dim_theme_hierarchy` | One row per theme | `theme_key` (INTEGER) | Theme hierarchy with resolved parent/root names and depth |
| `dim_set` | One row per set | `set_key` (STRING) | Sets enriched with theme info and pre-aggregated inventory metrics |
| `dim_part` | One row per part | `part_key` (STRING) | Parts with category, production year range, and active status |
| `dim_color` | One row per colour | `color_key` (INTEGER) | Colours with RGB, transparency flag, and derived colour family |

### Facts

| Table | Grain | Composite Key | Description |
|---|---|---|---|
| `fct_set_inventory` | One row per part-colour in an inventory | `inventory_id` + `part_key` + `color_key` | Detailed bill-of-materials for each set |
| `fct_set_minifigs` | One row per minifigure in a set | `set_key` + `minifig_key` | Minifigures included in each set |
| `fct_set_composition` | One row per set | `set_key` | Set-level aggregate metrics (unique parts, colours, transparency %, spare %, dominant colour/category) |
| `fct_color_usage` | One row per colour | `color_key` | Colour-level usage metrics across the catalogue |
| `fct_part_usage` | One row per part | `part_key` | Part-level usage metrics across sets and themes |
| `fct_theme_summary` | One row per theme | `theme_key` | Theme-level aggregate metrics (total sets, avg parts, year span) |
