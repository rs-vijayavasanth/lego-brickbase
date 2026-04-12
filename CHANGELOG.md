# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Logical data model diagram (Mermaid ERD) covering all dimension and fact tables in the gold layer

### Fixed
- `fct_theme_summary`: replaced `theme_name` as primary key with `theme_key` (INTEGER surrogate key), grouping and selecting by `theme_key` to ensure uniqueness

## [0.7.0] - 2026-04-08

### Added
- Gold layer Databricks notebooks for all dimensional models:
  - Dimensions: `dim_color`, `dim_part`, `dim_set`, `dim_theme_hierarchy`
  - Facts: `fct_color_usage`, `fct_part_usage`, `fct_set_composition`, `fct_set_inventory`, `fct_set_minifigs`, `fct_theme_summary`
- Delta table constraints including primary keys, foreign key references, and parent key constraints
- Table and column descriptions on all gold layer Delta tables

### Changed
- Harmonized key column naming across `dim_set`, `fct_set_inventory`, and `fct_set_minifigs`
- Removed low-quality (`bad DQ`) columns from `dim_part`

## [0.6.0] - 2026-04-07

### Added
- Silver layer Databricks notebooks for all foundation models:
  - Colors, Themes, Sets, Parts, Part Categories, Minifigs
  - Inventories, Inventory Parts, Inventory Minifigs, Inventory Sets
- PySpark-based transformations with key and column aliasing
- Delta table creation using CREATE OR REPLACE for idempotent loads

## [0.5.0] - 2026-04-06

### Added
- Bronze layer Databricks notebooks for ingesting all LEGO datasets:
  - API-sourced: Colors, Themes, Sets, Parts, Part Categories, Minifigs
  - CSV-sourced: Inventories, Inventory Parts, Inventory Minifigs, Inventory Sets
- Delta table creation and loading support in ingestion notebooks
- Markdown documentation cells added to ingestion notebooks

### Changed
- Renamed ingestion folder from `databricks/ingestion/` to `databricks/bronze/` to align with medallion architecture naming
- Updated notebooks to retrieve API credentials via Databricks secrets

## [0.4.0] - 2026-04-06

### Added
- Conceptual data model diagram

### Changed
- Renamed fact entities from plural to singular form

## [0.3.0] - 2026-04-06

### Added
- Domain solution design documentation
- Solution design diagram
- Domain model diagram

## [0.2.0] - 2026-04-05

### Changed
- Replaced dbt with PySpark for data transformation
- Restructured project folder layout

## [0.1.0] - 2026-04-04

### Added
- Initial project setup
- README with project purpose and design overview
- Pull request template
