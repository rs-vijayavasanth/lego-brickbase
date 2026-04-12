# Deployment

[< Back to Solution Outline](README.md)

---

## Current Deployment Model

The project currently follows a **manual notebook execution** model on Databricks:

| Aspect | Approach |
|---|---|
| Execution | Manual notebook runs in the Databricks workspace |
| Ordering | Engineer runs notebooks in layer order (Bronze → Silver → Gold) |
| Environment | Single Databricks workspace (development) |
| Source Control | Git-based via GitHub with pull request reviews |
| Artifact Management | Notebooks synced from GitHub to Databricks workspace |

---

## Infrastructure Components

| Component | Configuration |
|---|---|
| Databricks Workspace | Single workspace with Unity Catalog enabled |
| Compute Cluster | Shared or single-node cluster for notebook execution |
| External Volumes | Three volumes under `lego_brickbase`: `bronze`, `silver`, `gold` |
| Unity Catalog | Catalog `lego_brickbase` with schemas: `bronze`, `silver`, `gold` |
| Secrets Scope | `rebrickable` scope containing `api-key` |

---

## Recommended Future Deployment

For production readiness, the following deployment enhancements are recommended:

1. **Databricks Workflows** - Orchestrate notebook execution as a multi-task job with dependencies matching the execution graph in [Data Pipeline - Execution Dependencies](07-data-pipeline.md#execution-dependencies)
2. **Scheduled Triggers** - Daily or weekly job triggers to refresh data from the Rebrickable API
3. **Environment Promotion** - Separate DEV / STAGING / PROD workspaces with Unity Catalog cross-workspace sharing
4. **CI/CD Pipeline** - GitHub Actions workflow for:
   - Notebook linting and validation on pull request
   - Automated deployment to Databricks workspace on merge to `main`
   - Integration tests against a test catalog
