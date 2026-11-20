# DPDP360 Compliance Engine Implementation Plan

> Use the approved design specification as authority. Implement test-first, commit each completed task, and require independent spec and quality review.

**Goal:** Deliver versioned regulatory controls, readiness assessments, evidence traceability, findings, remediation and management reporting.

**Architecture:** Regulatory definitions are versioned independently of tenant assessment instances. Each assessment pins a catalogue version and assessment date. Tenant answers, evidence, findings and remediation remain in the tenant database.

**Stack:** FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, Next.js, TypeScript, pytest, Playwright.

**Spec:** `../specs/2026-11-20-dpdp360-design-spec-v1.md`

## Global constraints

- Pravidhi Tech Solutions LLP owns all product IP and commercialization.
- Separate PostgreSQL database and credentials per SaaS tenant; server-side tenant resolution only.
- Modular monolith first; independently deployable workers.
- Sensitive transitions are authorized and audited. AI cannot independently set official compliance status.
- Regulatory mappings require authoritative provenance and qualified legal review before production.
- No secrets or real personal data in tests, logs or CI artifacts.
- Use test-first implementation and commit every completed task.

## Review focus

1. Tenant IDOR and cross-tenant evidence access.
2. Effective-date, amendment, exemption and supersession correctness.
3. Assessment snapshot immutability and deterministic scoring.
4. Evidence upload abuse, malware and object-reference authorization.
5. Concurrent remediation updates and duplicate worker delivery.

## Proposed file map

- `services/api/app/regulatory/`: source, requirement, version and applicability models.
- `services/api/app/assessments/`: templates, questions, responses and immutable snapshots.
- `services/api/app/evidence/`: metadata, object storage, versions and review state.
- `services/api/app/findings/` and `services/api/app/remediation/`.
- `services/api/app/reports/readiness.py`.
- Matching Next.js features under `apps/web/src/features/`.
- Unit, integration, security and Playwright E2E tests.

## Interfaces

- `resolve_requirement(requirement_id: UUID, as_of: date, catalogue_version: str) -> RequirementSnapshot`
- `create_assessment(tenant: TenantContext, template_id: UUID, as_of: date) -> Assessment`
- `record_answer(assessment_id: UUID, question_id: UUID, answer: AnswerPayload, actor: Principal) -> AssessmentResponse`
- `calculate_readiness(assessment_id: UUID) -> ReadinessResult`
- `create_finding(assessment_id: UUID, control_snapshot_id: UUID, severity: Severity, evidence_refs: list[UUID]) -> Finding`
- `review_evidence(evidence_id: UUID, reviewer: Principal, decision: EvidenceDecision, notes: str | None) -> EvidenceReview`

## Tasks

### 1. Regulatory catalogue and provenance
- [ ] Test effective-date boundaries, future/expired requirements, exemptions, amendments and supersession chains.
- [ ] Implement authoritative source metadata, citation locator, publication/effective dates, applicability, version and legal-review status.
- [ ] Ensure future or superseded rules are never silently applied.
- [ ] Keep unreviewed fixtures explicitly illustrative.
- [ ] Verify with `pytest tests/unit/regulatory -q`; commit `feat: add versioned regulatory catalogue`.

### 2. Assessment templates and snapshots
- [ ] Test industry template selection, question ordering, required fields and snapshot immutability.
- [ ] Pin every assessment to catalogue version and assessment date.
- [ ] Verify with `pytest tests/integration/assessments/test_templates.py -q`; commit `feat: add readiness assessment templates`.

### 3. Responses and deterministic scoring
- [ ] Test unanswered, not-applicable, partial and compliant responses, weighting and evidence-required controls.
- [ ] Implement typed answers and deterministic scoring.
- [ ] Prevent AI from writing approved answers without authorized human action.
- [ ] Verify with `pytest tests/unit/assessments -q`; commit `feat: implement assessment scoring`.

### 4. Evidence lifecycle
- [ ] Test file allowlist/size, duplicate uploads, versions, reviewer permissions, rejection and expiry.
- [ ] Implement tenant-scoped object references, short-lived grants, malware-scan status and review decisions.
- [ ] Verify with `pytest tests/integration/evidence -q`; commit `feat: add evidence lifecycle`.

### 5. Findings and remediation
- [ ] Test traceability, severity, assignment, due dates, state transitions, reopen and idempotency.
- [ ] Implement authorized state machines and audit events.
- [ ] Verify with `pytest tests/integration/remediation -q`; commit `feat: add findings and remediation tracking`.

### 6. Reports and dashboard
- [ ] Test report totals against source responses, excluded controls, stale evidence and role visibility.
- [ ] Implement traceable API projection and dashboard.
- [ ] Add E2E assessment → evidence → review → finding/report path.
- [ ] Verify with `pytest -q` and Playwright readiness tests; commit `feat: add readiness dashboard and reports`.

## Exit criteria

- Assessment snapshots are reproducible against pinned catalogue version and date.
- Every finding traces to a versioned control and evidence.
- Unreviewed regulatory mappings are never presented as legally approved.
- Reports are deterministic and role-scoped.