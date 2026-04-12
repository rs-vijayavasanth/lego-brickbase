# Security

[< Back to Solution Outline](README.md)

---

## Authentication and Secrets

| Concern | Implementation |
|---|---|
| API Key Storage | Databricks Secrets (`scope: rebrickable`, `key: api-key`). Never stored in notebooks or version control. |
| API Authentication | Key passed via HTTP `Authorization` header per request |
| Databricks Access | Workspace authentication via Databricks-managed identity or SSO |

---

## Data Access Control

| Layer | Access Policy |
|---|---|
| Bronze | Restricted to data engineers; contains raw, unvalidated data |
| Silver | Accessible to data engineers and analysts; cleansed and conformed |
| Gold | Broadly accessible; designed for reporting and self-service analytics |

Unity Catalog provides fine-grained access control at the catalog, schema, and table level. Table-level grants can be configured to restrict sensitive data.

---

## Network and Transport

| Concern | Implementation |
|---|---|
| API Communication | HTTPS/TLS for all Rebrickable API calls |
| Databricks Platform | Platform-managed network isolation and encryption at rest |
| Power BI Connectivity | Secure Databricks SQL endpoint with token-based authentication |

---

## Data Sensitivity

This project works exclusively with **publicly available LEGO product data** from Rebrickable. The dataset contains no personally identifiable information (PII), financial data, or otherwise sensitive content. The primary security concerns are:

- Protecting the Rebrickable API key from exposure
- Ensuring appropriate access controls on the Databricks workspace
- Maintaining audit trails via SCD2 metadata columns
