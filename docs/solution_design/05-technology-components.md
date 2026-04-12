# Technology Components

[< Back to Solution Outline](README.md)

---

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Data Platform | **Databricks** | Unified analytics platform for compute, storage, and governance |
| Storage Format | **Delta Lake** | ACID-compliant lakehouse storage with schema enforcement, time travel, and merge support |
| Compute Engine | **Apache Spark (PySpark)** | Distributed data processing for transformations and aggregations |
| Catalog | **Unity Catalog** | Centralised metadata, access control, and data lineage |
| Secrets Management | **Databricks Secrets** | Secure storage of API credentials (`scope: rebrickable`) |
| Storage | **External Volumes** | Unity Catalog-managed file storage for raw data and Delta tables |
| Development | **Databricks Notebooks** | Interactive development environment (Jupyter-compatible `.ipynb`) |
| Reporting | **Power BI** | Business intelligence and interactive dashboarding |
| Version Control | **Git / GitHub** | Source control, pull requests, and change management |

---

## Component Interactions

```
┌────────────────────────┐
│   Rebrickable API/CSV  │  (External Data Source)
└──────────┬─────────────┘
           │ HTTPS / File Upload
           ▼
┌────────────────────────────────────────────────────────┐
│                    Databricks                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Bronze     │  │   Silver     │  │    Gold      │ │
│  │  Notebooks   │─▶│  Notebooks   │─▶│  Notebooks   │ │
│  │  (Ingest)    │  │  (Cleanse)   │  │  (Model)     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │         │
│         ▼                 ▼                  ▼         │
│  ┌────────────────────────────────────────────────┐    │
│  │          External Volumes (Delta Lake)         │    │
│  │  /Volumes/lego_brickbase/{bronze|silver|gold}  │    │
│  └────────────────────────────────────────────────┘    │
│                                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │              Unity Catalog                     │    │
│  │  lego_brickbase.{bronze|silver|gold}.*         │    │
│  └────────────────────────────────────────────────┘    │
│                          │                             │
│                    Databricks SQL                      │
└──────────────────────────┬─────────────────────────────┘
                           │ SQL Endpoint
                           ▼
                   ┌──────────────┐
                   │   Power BI   │
                   │  (Reports)   │
                   └──────────────┘
```
