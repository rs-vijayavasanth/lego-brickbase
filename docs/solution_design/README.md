# Solution Outline Document

| | |
|---|---|
| **Project** | LEGO Brickbase |
| **Version** | 1.0.0 |
| **Date** | 2026-04-12 |
| **Status** | Active Development |
| **Repository** | [rs-vijayavasanth/lego-brickbase](https://github.com/rs-vijayavasanth/lego-brickbase) |

---

## Table of Contents

| # | Section | Description |
|---|---|---|
| 1 | [Summary](#1-summary) | Purpose, business context, scope, and key decisions |
| 2 | [Contributors](#2-contributors) | Project team and responsibilities |
| 3 | [Solution Architecture](01-solution-architecture.md) | High-level architecture, layer responsibilities, and data flow |
| 4 | [Conceptual Data Model](02-conceptual-data-model.md) | Domain model and conceptual entity relationships |
| 5 | [Core Data Building Blocks](03-core-data-building-blocks.md) | Source entities, Bronze, Silver, and Gold layer tables |
| 6 | [Logical Data Model](04-logical-data-model.md) | ER diagram, key relationships, and constraint strategy |
| 7 | [Technology Components](05-technology-components.md) | Technology stack and component interactions |
| 8 | [Integration](06-integration.md) | Rebrickable API, CSV ingestion, and Power BI integration |
| 9 | [Data Pipeline](07-data-pipeline.md) | Pipeline stages, ingestion patterns, and execution dependencies |
| 10 | [Deployment](08-deployment.md) | Current deployment model and future recommendations |
| 11 | [Security](09-security.md) | Authentication, access control, and data sensitivity |
| 12 | [Governance and Compliance](10-governance-and-compliance.md) | Data quality, lineage, change management, and naming conventions |
| 13 | [Non-Functional Requirements](11-non-functional-requirements.md) | Performance, scalability, reliability, and maintainability |
| 14 | [Future Considerations](12-future-considerations.md) | Planned enhancements and roadmap areas |

---

## 1. Summary

### 1.1 Purpose

LEGO Brickbase is a data engineering project that demonstrates the complete workflow of integrating LEGO brick data from the [Rebrickable](https://rebrickable.com/) API and database into a unified analytical data model on Databricks. The solution covers data ingestion, transformation with PySpark, dimensional modeling, and tabular modeling for Power BI reporting.

### 1.2 Business Context

The LEGO ecosystem consists of thousands of sets, parts, colours, themes, and minifigures with complex relationships between them. Rebrickable maintains a comprehensive open dataset that catalogues this information. This project transforms that raw data into an analytics-ready data warehouse that supports questions such as:

- Which themes have the most sets and parts over time?
- What is the colour composition of a given set?
- Which parts appear across the most sets and themes?
- How do sets compare in complexity (unique parts, colours, minifigures)?

### 1.3 Scope

| In Scope | Out of Scope |
|---|---|
| Ingestion from Rebrickable REST API (v3) | Real-time / streaming ingestion |
| Ingestion from Rebrickable CSV exports | User-contributed data or MOC (My Own Creation) sets |
| Medallion architecture (Bronze, Silver, Gold) | Machine learning or predictive analytics |
| Dimensional modeling for analytical queries | Multi-tenant or multi-environment deployment |
| Power BI semantic model and reporting | Automated alerting and monitoring |
| Unity Catalog registration and governance | Data sharing or marketplace publishing |

### 1.4 Key Decisions

| Decision | Rationale |
|---|---|
| PySpark over dbt | Full control over transformations within the Databricks notebook environment; removed the need for an additional tool in the stack (changed in v0.2.0) |
| SCD Type 2 in Bronze | Preserves full history of changes from the source system, enabling point-in-time analysis and audit |
| Delta Lake throughout | ACID transactions, schema enforcement, time travel, and seamless Unity Catalog integration |
| Surrogate keys in Gold | Stable join keys decoupled from source natural keys, improving resilience to upstream changes |

---

## 2. Contributors

| Name | Role | Responsibility |
|---|---|---|
| RS Vijayavasanth | Data Engineer / Architect | Solution design, data modeling, pipeline development, documentation |
