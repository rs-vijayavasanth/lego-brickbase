# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
