# Future Considerations

[< Back to Solution Outline](README.md)

---

The following enhancements are potential areas for future development:

| Area | Enhancement | Benefit |
|---|---|---|
| **Orchestration** | Databricks Workflows with dependency-aware multi-task jobs | Automated end-to-end pipeline execution with retry and alerting |
| **CI/CD** | GitHub Actions for notebook validation, linting, and automated deployment | Reduced manual effort and increased deployment confidence |
| **Testing** | Data quality checks (Great Expectations or Databricks DQ rules) on Silver and Gold tables | Automated detection of data anomalies and schema drift |
| **Monitoring** | Pipeline execution dashboards and alerting on failures or data freshness SLAs | Proactive incident detection |
| **Incremental Loads** | Incremental ingestion using `last_modified_dt` watermarks in Bronze | Reduced API calls and faster refresh cycles |
| **Additional Sources** | BrickLink, BrickOwl, or LEGO.com price data | Enriched analytics with market pricing and availability |
| **Environments** | DEV / STAGING / PROD workspace separation with promotion workflows | Safe testing of changes before production deployment |
| **Semantic Layer** | Databricks AI/BI Dashboard or published Unity Catalog metrics | Self-service analytics without Power BI dependency |
