# Deployment contract

## Bootstrap boundary

Provision these account/workspace foundations outside the bundle, preferably with Terraform and account-level APIs:

- workspace, metastore attachment, storage credentials, external locations, and network/private-link configuration
- service principal and its workspace assignment; CI OAuth credentials stored in the CI secret store
- groups (`data-platform-admins`, `data-engineers`, `analytics-readers`, `data-platform-operators`, `data-platform-readers`)
- catalog with environment-specific storage root and ownership
- cluster policy and SQL warehouse entitlement/limits
- secret scope backed by the cloud secret manager, plus narrowly scoped access grants

Bundle variables deliberately do not include secret values. Workloads retrieve credentials at runtime through secret references. Avoid printing secret values or placing them in job parameters, notebooks, logs, or state files.

## Workspace topology

Use separate dev, staging, and prod workspaces for isolation. Each target has a distinct host, catalog, secret scope, service principal, and data storage boundary. For larger organizations, split workspaces by persona or domain, then define explicit workspace/catalog grants and a deployment target for each workspace. Keep production writes limited to the release identity and approved operators.

## CI/CD stages

```text
pull request -> lint/build -> bundle validate -> unit checks
  -> merge to main -> deploy dev -> integration/data-quality checks
  -> release approval -> deploy same commit to staging -> acceptance checks
  -> production approval -> deploy same commit to prod -> smoke checks
```

Set `DATABRICKS_HOST` and `DATABRICKS_CLIENT_ID` in each isolated CI environment, and use Databricks OAuth federation or short-lived OAuth credentials. Do not reuse a human PAT. Pass `--target` explicitly in automation. Restrict production deployment to protected branches and approved release identities.

## Bundle notes

The example bundle intentionally uses environment variables for workspace host, service principal, sizing, and catalog name. Replace example values with actual workspace-compatible values. Catalog creation is outside the bundle because metastore, storage root, and account setup need tenant-specific decisions. The bundle creates bronze/silver/gold schemas and their grants under an existing catalog.

The warehouse and cluster examples use supported settings that can vary by cloud and workspace. Validate against the actual Databricks CLI and workspace before deployment. Policies should cap node types, workers, runtime versions, and cost. Prefer ephemeral job compute for ETL; use SQL warehouses for interactive analytics.
