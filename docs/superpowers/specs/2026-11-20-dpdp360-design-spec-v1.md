# DPDP360 Design Specification v1.0

**Product owner:** Pravidhi Tech Solutions LLP  
**Status:** Approved product and architecture decisions.

## Goal

Build DPDP360, an AI-assisted DPDP compliance and privacy-operations platform for Indian organizations, supporting readiness assessment followed by continuous compliance management.

## Product scope

- Organization onboarding, tenant management, departments, RBAC and subscription entitlements.
- Readiness assessments with industry question sets, applicability, legal mapping, evidence, findings, remediation, reviews and reports.
- Personal-data inventory and processing activities, including purposes, fiduciary/processor relationships, data flows, retention and sharing.
- Purpose-specific consent and notice versioning, event history and withdrawal.
- Data Principal request workflows: identity verification, access-related requests, correction/updating, erasure, withdrawal, grievances, deadlines and evidence.
- Breach/incident workflows: impact assessment, timeline, escalation, notification preparation, human authorization and post-incident review.
- Vendor/processor register, questionnaires, DPAs/contracts, risk scoring and remediation.
- Compliance control register, evidence validity/review, approvals, audit exports and dashboards.
- AI Privacy Copilot for document analysis, evidence-gap detection, drafting, vendor analysis, remediation suggestions and reporting.
- Later integrations and private enterprise deployment.

## Architecture

A modular monolith initially, with independently deployable workers. The central control plane stores tenant registry, subscription and provisioning metadata only. Each SaaS tenant has a separate PostgreSQL database and credentials. Enterprise deployments use dedicated infrastructure and a dedicated database. Tenant routing is server-side and must never trust browser-supplied tenant IDs or connection strings.

## Technology direction

- Web: Next.js, TypeScript, Tailwind CSS, shadcn/ui.
- API: Python FastAPI, SQLAlchemy, Alembic, Pydantic.
- Data/jobs: PostgreSQL, Redis, Celery.
- Retrieval: pgvector; object storage via S3-compatible interface.
- AI: provider-independent internal gateway; self-hosted open-source models. Ollama may support early development; vLLM is a candidate for GPU production after benchmark.
- Packaging: Docker; initial deployment on Pravidhi VPS; cloud-ready configuration.
- API prefix: `/api/v1`.

## Security and governance

- OIDC-compatible authentication; MFA for privileged accounts.
- RBAC and scoped permissions, enforced on the server.
- Per-tenant DB credentials, encryption in transit/at rest, managed secrets.
- Append-only/tamper-evident audit events.
- Short-lived file access links and malware scanning.
- SSRF controls, prompt-injection defenses, secure sessions and rate limits.
- Automated tenant-isolation negative tests.
- SAST, DAST, dependency scanning, encrypted backups and tested per-tenant restore.
- AI may analyze, recommend, draft and create draft tasks. It may not independently change official compliance status, delete personal data or submit external notifications.
- Record model/version, prompt version, source/evidence references, output/confidence, reviewer decision and execution result.

## Regulatory and legal design

Support DPDP Act 2023, DPDP Rules 2025, commencement notifications, exemptions, amendments and directions through a versioned regulatory catalogue. Each requirement records authoritative source/citation, effective date, applicability, evidence requirements and supersession history. Qualified legal review is required before regulatory mappings become production controls. The product supports compliance management; it does not replace legal advice or guarantee compliance.

## Initial API resource groups

`/organizations`, `/assessments`, `/compliance/controls`, `/compliance/findings`, `/remediation/tasks`, `/data-assets`, `/processing-activities`, `/consents`, `/data-principal-requests`, `/vendors`, `/incidents`, `/evidence`, `/ai/assist`, `/approvals`, `/audit-events`.

## MVP acceptance criteria

1. Organization registers and receives a provisioned tenant database.
2. Tenant isolation is proven with automated negative tests.
3. An authorized user completes a readiness assessment.
4. Findings are traceable to versioned controls and source material.
5. Remediation can be assigned and tracked.
6. Evidence can be uploaded, reviewed and versioned.
7. Management dashboard reports readiness and outstanding work.
8. AI can analyze evidence and propose recommendations.
9. Consequential actions require explicit human approval and backend authorization.
10. Per-tenant backup and restore are tested.
