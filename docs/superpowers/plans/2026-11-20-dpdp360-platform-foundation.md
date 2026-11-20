# DPDP360 Platform Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish secure identity, organization onboarding, tenant provisioning, per-tenant database isolation, authorization and auditable platform primitives.

**Architecture:** A FastAPI modular monolith and Next.js application use a control-plane database only for tenant metadata. Tenant business data is accessed through a server-side tenant database resolver. Provisioning and migrations run through controlled worker jobs.

**Tech Stack:** Python 3.12+, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL, Redis, Celery, Next.js, TypeScript, pnpm, Docker

**Spec:** `../specs/2026-11-20-dpdp360-design-spec-v1.md`

## Global Constraints

- Product IP, source, architecture, infrastructure, deployment, operations and commercialization are owned by Pravidhi Tech Solutions LLP.
- SaaS tenant business data is isolated in a separate PostgreSQL database with separate credentials per tenant.
- Tenant routing and authorization are server-side; never trust client-supplied tenant identifiers or database connection strings.
- Modular monolith first; independently deployable workers; no premature service extraction.
- Human approval is mandatory for consequential AI-assisted actions; AI is not an authorization authority.
- All sensitive state transitions are authorized and audited.
- Regulatory mappings are versioned and require qualified legal approval before production.
- No secrets or real personal data in tests, logs, fixtures or CI artifacts.
- Implement test-first, run the specified verification command, and commit each completed task.

## Review Focus

1. **Tenant confusion / IDOR:** a user guesses another tenant's resource ID; request must be denied and audited. Add negative tests to the tenant authorization task.
2. **Provisioning partial failure:** database creation succeeds but registry/secret setup fails; provisioning must be idempotent, recoverable and leave no usable orphan. Add fault-injection tests to provisioning task.
3. **Concurrent updates / retries:** duplicate requests or worker retries must not duplicate consequential state transitions. Add idempotency/concurrency tests to the owning workflow task.
4. **Untrusted files / payloads:** malformed, oversized or hostile content must be rejected or sandboxed without SSRF, code execution or cross-tenant leakage. Add adversarial fixtures to ingestion/upload tasks.
5. **Regulatory time/version ambiguity:** a control effective only for a future/past period must not be applied to the wrong assessment date. Add effective-date and supersession tests to regulatory catalogue tasks.

---

## Proposed file map

- Create `services/api/app/main.py` — FastAPI application and router registration.
- Create `services/api/app/core/config.py` — typed environment configuration and validation.
- Create `services/api/app/core/security.py` — token validation and principal extraction.
- Create `services/api/app/control_plane/models.py` — tenant registry and provisioning state only.
- Create `services/api/app/tenancy/resolver.py` — server-side tenant DB resolution.
- Create `services/api/app/tenancy/provisioning.py` — idempotent tenant DB provisioning.
- Create `services/api/app/authz/policy.py` — RBAC/scoped authorization primitives.
- Create `services/api/app/audit/events.py` — append-only audit event interface.
- Create `services/worker/app/tasks/provision_tenant.py` — provisioning worker task.
- Create `services/api/alembic/control_plane/` and `services/api/alembic/tenant/` — separate migration streams.
- Create `tests/unit/tenancy/`, `tests/integration/tenancy/`, `tests/security/test_tenant_isolation.py`.
- Create `.env.example`, `compose.yaml`, `pyproject.toml`, `package.json`, `.github/workflows/ci.yml`.

## Interfaces

- `TenantContext(tenant_id: UUID, database_key: str, status: TenantStatus)` is created only by trusted server-side resolution.
- `resolve_tenant_context(principal: AuthenticatedPrincipal, requested_org: UUID) -> TenantContext` verifies membership and active status before resolving a database.
- `provision_tenant(tenant_id: UUID, idempotency_key: str) -> ProvisioningResult` is safe to retry and records each stage.
- `authorize(principal: AuthenticatedPrincipal, action: str, resource: ResourceContext) -> None` raises a typed authorization error on denial.
- `append_audit_event(event: AuditEvent) -> None` writes an append-only event with actor, tenant, action, target, timestamp and correlation ID.

### Task 1: Establish project skeleton and CI

**Files:** create paths listed above for app entrypoints, config, package manifests, CI and initial tests.

- [ ] Write failing smoke tests asserting API health endpoint returns 200 and invalid required configuration prevents startup.
- [ ] Run `pytest tests/unit/test_health.py -q`; expected: FAIL before implementation.
- [ ] Implement FastAPI app factory, `/health/live`, typed settings and frontend scripts.
- [ ] Add CI jobs for Python lint/type/test and frontend lint/type/build.
- [ ] Run `ruff check .`, `mypy services/api`, `pytest -q`, `pnpm lint`, `pnpm typecheck`, `pnpm build`; expected: PASS.
- [ ] Commit `chore: bootstrap dpdp360 platform`.

### Task 2: Implement identity principal and organization membership

**Files:** `services/api/app/core/security.py`, `services/api/app/organizations/`, `tests/unit/auth/`, `tests/integration/organizations/`.

- [ ] Write tests for valid token, expired token, invalid issuer/audience, missing subject and inactive membership.
- [ ] Run targeted tests; expected: FAIL.
- [ ] Implement OIDC-compatible JWT verification using configured issuer/audience and trusted key discovery; never accept unsigned or algorithm-confused tokens.
- [ ] Implement organization membership lookup and typed `AuthenticatedPrincipal`.
- [ ] Run `pytest tests/unit/auth tests/integration/organizations -q`; expected: PASS.
- [ ] Commit `feat: add identity and organization membership`.

### Task 3: Build control-plane tenant registry

**Files:** `control_plane/models.py`, `alembic/control_plane/`, `tests/integration/control_plane/`.

- [ ] Test tenant lifecycle states `pending`, `provisioning`, `active`, `failed`, `suspended`; assert invalid transitions fail.
- [ ] Run targeted tests; expected: FAIL.
- [ ] Implement tenant registry, unique slug, immutable tenant identifier, provisioning state and database-secret reference. Do not store tenant business records here.
- [ ] Add Alembic migration and rollback test.
- [ ] Run control-plane integration tests; expected: PASS.
- [ ] Commit `feat: add control plane tenant registry`.

### Task 4: Provision isolated tenant PostgreSQL databases

**Files:** `tenancy/provisioning.py`, `worker/app/tasks/provision_tenant.py`, `alembic/tenant/`, `tests/integration/tenancy/test_provisioning.py`.

- [ ] Test successful provisioning, duplicate idempotency key, concurrent duplicate jobs, database-create failure, secret-store failure and migration failure.
- [ ] Run targeted tests; expected: FAIL.
- [ ] Implement a staged provisioning state machine: reserve tenant → create DB/user → store secret reference → apply tenant migrations → verify connectivity → activate tenant.
- [ ] Ensure retry resumes safely or compensates; never mark tenant active before verification.
- [ ] Run `pytest tests/integration/tenancy/test_provisioning.py -q`; expected: PASS including injected failures.
- [ ] Commit `feat: provision isolated tenant databases`.

### Task 5: Enforce tenant routing and authorization

**Files:** `tenancy/resolver.py`, `authz/policy.py`, `tests/security/test_tenant_isolation.py`.

- [ ] Test cross-tenant resource IDs, forged organization headers, stale membership, suspended tenant, mismatched worker context and direct DB-key injection.
- [ ] Run security tests; expected: FAIL.
- [ ] Implement request-scoped tenant context derived from authenticated principal plus verified membership; reject client-supplied DB routing fields.
- [ ] Ensure repository/session factories require `TenantContext`; no global tenant DB session.
- [ ] Run `pytest tests/security/test_tenant_isolation.py -q`; expected: PASS with every cross-tenant attempt denied.
- [ ] Commit `feat: enforce tenant scoped data access`.

### Task 6: RBAC and append-only audit foundation

**Files:** `authz/policy.py`, `audit/events.py`, `tests/unit/authz/`, `tests/integration/audit/`.

- [ ] Test least-privilege role matrix, denied-by-default behavior, scoped permissions and audit immutability.
- [ ] Run targeted tests; expected: FAIL.
- [ ] Implement roles/permissions and append-only audit writes with actor, tenant, action, resource, timestamp and correlation ID.
- [ ] Add tests proving application roles cannot update/delete prior audit events.
- [ ] Run targeted tests; expected: PASS.
- [ ] Commit `feat: add authorization and audit primitives`.

## Exit criteria

- Organization onboarding creates a tenant registry entry and a separately credentialed PostgreSQL database.
- Tenant DB routing is exclusively server-side.
- Automated negative tests prove no cross-tenant read/write path through HTTP or worker execution.
- Provisioning retries and partial failures are recoverable.
- CI gates are green.
