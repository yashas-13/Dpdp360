# DPDP360 Enterprise Operations Implementation Plan

> Use the approved design specification as authority. Implement test-first, commit each completed task, and require independent spec and quality review.

**Goal:** Deliver secure SaaS/enterprise deployment, observability, backup/restore, release engineering and production security hardening.

**Architecture:** Dockerized modular monolith and independent workers. SaaS deployment provisions isolated tenant databases. Enterprise deployment uses dedicated infrastructure and database. Environment-specific configuration and secrets are externalized.

**Stack:** Docker, Compose, Nginx, PostgreSQL, Redis, FastAPI, Next.js, Linux systemd or container orchestration, CI security tooling.

**Spec:** `../specs/2026-11-20-dpdp360-design-spec-v1.md`

## Global constraints

- Pravidhi Tech Solutions LLP owns infrastructure, deployment and operations.
- No secrets in Git, images, logs, CI artifacts or support bundles.
- SaaS tenants have separate PostgreSQL databases and credentials.
- Enterprise deployment is isolated and separately configured.
- All privileged operations are authorized and audited.
- Backups are encrypted and restores are tested, not merely configured.

## Review focus

- Container privilege, exposed ports, network segmentation and secret injection.
- Tenant backup/restore selecting the wrong database or storage prefix.
- Backup encryption, key rotation, retention and restore verification.
- Migration rollback, deployment health checks and release provenance.
- Log redaction, PII exposure, alert fatigue and audit integrity.

## Proposed file map

- `infra/compose/saas.yaml` and `infra/compose/enterprise.yaml`.
- `infra/nginx/` for TLS termination, routing and security headers.
- `infra/scripts/` for environment provisioning, tenant backup and restore.
- `services/api/app/observability/` and worker health endpoints.
- `.github/workflows/security.yml`, `release.yml` and staging deployment.
- `docs/operations/runbooks/` for incident, backup, restore, key rotation, upgrade and rollback.
- Operations integration tests and deployment smoke tests.

## Tasks

### 1. Deployment topology and hardening
- [ ] Define non-root containers, read-only filesystems where practical, dropped capabilities, resource limits and health checks.
- [ ] Segment public ingress, application, worker, database and Redis networks.
- [ ] Expose only required TLS ingress; databases and Redis are never public.
- [ ] Validate SaaS and enterprise Compose configurations; commit `infra: add hardened deployment topologies`.

### 2. Secrets and environment configuration
- [ ] Define typed configuration and fail-closed startup validation.
- [ ] Inject secrets from an approved secret store or protected runtime files; never bake secrets into images.
- [ ] Document rotation and emergency revocation.
- [ ] Add secret scanning and config tests; commit `security: harden runtime configuration`.

### 3. Observability and operational controls
- [ ] Add structured logs, correlation IDs, metrics and traces.
- [ ] Redact credentials, tokens and personal data; scope tenant-level telemetry.
- [ ] Add API and worker liveness/readiness checks and actionable alerts.
- [ ] Verify redaction and health tests; commit `feat: add production observability`.

### 4. Backup and restore
- [ ] Encrypt backups, isolate storage credentials and enforce retention.
- [ ] Test per-tenant backup selection, restore to isolated target, integrity checks and recovery evidence.
- [ ] Add restore drills and documented RPO/RTO targets only after business approval.
- [ ] Verify failure injection and cross-tenant restore tests; commit `feat: add tenant backup and restore`.

### 5. Release, migration and rollback
- [ ] Build reproducible images and record provenance/SBOM.
- [ ] Gate releases on unit, integration, E2E, SAST, dependency and container scans.
- [ ] Test forward migration, rollback strategy, health-gated rollout and rollback.
- [ ] Commit `ci: add secure release pipeline`.

### 6. Security verification and runbooks
- [ ] Run threat-model review and authenticated DAST against staging.
- [ ] Verify tenant isolation, SSRF, access control, upload, session and audit regression suites.
- [ ] Write incident response, backup/restore, key rotation, upgrade and rollback runbooks.
- [ ] Complete independent whole-branch security review; commit `docs: add production operations runbooks`.

## Exit criteria

- SaaS and enterprise deployments are reproducible and isolated.
- Secrets are externalized and rotated through documented procedures.
- Backup/restore is demonstrated per tenant.
- CI blocks release on security/test failures.
- Operational runbooks and recovery evidence are available.