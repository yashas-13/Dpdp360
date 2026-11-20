# DPDP360 Privacy Operations Implementation Plan

> Use the approved design specification as authority. Implement test-first, commit each completed task, and require independent spec and quality review.

**Goal:** Implement data inventory, processing activities, consent, Data Principal requests, vendor/processor risk and breach workflows.

**Architecture:** Each workflow is a bounded module sharing tenant-scoped persistence, RBAC and append-only audit primitives. State machines and idempotency protect deadline-sensitive or externally consequential actions.

**Stack:** FastAPI, SQLAlchemy, PostgreSQL, Redis/Celery, Pydantic, Next.js, TypeScript, pytest, Playwright.

**Spec:** `../specs/2026-11-20-dpdp360-design-spec-v1.md`

## Global constraints

- Pravidhi Tech Solutions LLP owns all product IP and commercialization.
- Separate PostgreSQL database and credentials per SaaS tenant; server-side tenant resolution only.
- Modular monolith first; independently deployable workers.
- Consequential actions require human approval and backend authorization.
- All sensitive transitions are authorized and audited.
- Do not hardcode legal deadlines without a versioned, legally reviewed source.
- No secrets or real personal data in tests, logs or CI artifacts.

## Review focus

- Tenant IDOR, cross-tenant data leakage and object-reference authorization.
- Duplicate event delivery, idempotency and concurrent state transitions.
- Identity verification and erasure authorization.
- Legal deadline versioning and timezone boundaries.
- Incident notification drafts versus externally submitted notifications.

## Proposed file map

- `services/api/app/inventory/`: assets, categories, purposes, flows and retention.
- `services/api/app/consent/`: notices, consent records, versioning and withdrawal events.
- `services/api/app/rights/`: Data Principal intake, verification, workflow and deadlines.
- `services/api/app/vendors/`: processor register, questionnaires, contract references and risk.
- `services/api/app/incidents/`: breach lifecycle, timeline and notification drafts.
- `services/api/app/notifications/`: internal reminders and escalation.
- Matching web features and unit/integration/E2E tests.

## Interfaces

- `register_data_asset(payload: DataAssetCreate, actor: Principal) -> DataAsset`
- `record_consent(payload: ConsentCapture, actor: Principal) -> ConsentEvent`
- `withdraw_consent(consent_id: UUID, request: WithdrawalRequest, actor: Principal) -> ConsentEvent`
- `create_rights_request(payload: RightsRequestCreate, actor: Principal) -> RightsRequest`
- `transition_request(request_id: UUID, transition: RequestTransition, actor: Principal) -> RightsRequest`
- `assess_vendor(vendor_id: UUID, questionnaire: VendorAssessment, actor: Principal) -> VendorRiskResult`
- `record_incident_event(incident_id: UUID, event: IncidentEventCreate, actor: Principal) -> IncidentEvent`

## Tasks

### 1. Data inventory and processing activities
- [ ] Test categories, purpose linkage, fiduciary/processor roles, retention and flow graph validation.
- [ ] Implement tenant-scoped assets, activities, recipients, retention and source references.
- [ ] Keep discovery read-only; do not connect to customer systems or scan personal data without explicit authorization.
- [ ] Verify unit/integration suites; commit `feat: add personal data inventory`.

### 2. Notice and consent event ledger
- [ ] Test purpose-specific consent, notice version pinning, capture source/channel/time, withdrawal and immutable history.
- [ ] Derive current state from append-only events; add idempotency keys for duplicate delivery.
- [ ] Verify suites; commit `feat: add consent lifecycle`.

### 3. Data Principal rights requests
- [ ] Test intake, identity verification, request types, policy-versioned due dates, escalation and closure evidence.
- [ ] Implement request state machine and deadline scheduler; no global hardcoded legal timelines.
- [ ] Erasure is a separate approved action, never an automatic side effect of request creation or AI recommendation.
- [ ] Verify suites; commit `feat: add Data Principal request workflows`.

### 4. Vendor and processor risk
- [ ] Test questionnaire scoring, missing contracts, overdue reviews, risk acceptance and remediation.
- [ ] Implement register, role, DPA metadata, assessment responses and review history.
- [ ] Reuse evidence service for files; verify suites; commit `feat: add vendor processor risk`.

### 5. Breach and incident management
- [ ] Test timeline ordering, duplicate events, severity changes, notification drafts, approval denial and post-incident review.
- [ ] Implement incident records, impact assessment, escalation and evidence references.
- [ ] External submission remains disabled unless a separately authorized integration is explicitly approved.
- [ ] Verify suites; commit `feat: add breach incident workflow`.

### 6. Workspace and reminders
- [ ] Test tenant scope, retry safety, deduplication and suppression after closure.
- [ ] Implement queues for rights, consent, vendor reviews and incidents plus reminder worker.
- [ ] Add E2E rights-request and incident workflows.
- [ ] Verify all tests; commit `feat: add privacy operations workspace`.

## Exit criteria

- All workflows have auditable transitions and retry-safe processing.
- Consent history remains event-based.
- Legal deadlines are versioned and legally reviewed.
- Deletion and external notifications require explicit approval.