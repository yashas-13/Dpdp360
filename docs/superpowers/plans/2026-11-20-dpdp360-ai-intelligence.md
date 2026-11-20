# DPDP360 AI Intelligence Implementation Plan

> Use the approved design specification as authority. Implement test-first, commit each completed task, and require independent spec and quality review.

**Goal:** Deliver a secure self-hosted AI gateway, document analysis/retrieval, Privacy Copilot, human approval and model/output auditability.

**Architecture:** AI is isolated behind a provider-independent gateway and asynchronous worker pipeline. It receives only tenant-scoped, purpose-authorized context and returns proposals. Application policy and human approval control consequential execution.

**Stack:** Python, FastAPI, Celery, Redis, PostgreSQL, pgvector, object storage, Ollama for development, vLLM candidate for GPU production, Next.js.

**Spec:** `../specs/2026-11-20-dpdp360-design-spec-v1.md`

## Global constraints

- Pravidhi Tech Solutions LLP owns all product IP and commercialization.
- Separate PostgreSQL database and credentials per SaaS tenant; server-side tenant resolution only.
- AI is not an authorization authority; human approval is mandatory for consequential actions.
- No unrestricted SQL, shell, filesystem or arbitrary network tools.
- All sensitive state transitions are authorized and audited.
- No secrets or real personal data in tests, logs or CI artifacts.

## Review focus

- Prompt injection in uploaded/retrieved content and indirect instructions.
- Cross-tenant retrieval, citations and object-store access.
- SSRF, parser sandbox escapes, oversized/decompression-bomb files.
- AI overclaiming legal certainty or producing unsupported citations.
- Approval race conditions and execution-time reauthorization.

## Proposed file map

- `services/api/app/ai/gateway.py` and provider adapters.
- `services/api/app/ai/policy.py`, versioned prompts and `ai/audit.py`.
- `services/api/app/ingestion/` and `retrieval/`.
- `services/api/app/approvals/`.
- Worker tasks for ingestion and AI jobs.
- Security tests for prompt injection and tenant isolation; AI eval fixtures and E2E copilot tests.

## Interfaces

- `generate(request: ModelRequest) -> ModelResponse`
- `ingest_document(tenant: TenantContext, object_ref: ObjectRef, policy: IngestionPolicy) -> DocumentRecord`
- `retrieve_context(tenant: TenantContext, query: str, allowed_sources: list[UUID], limit: int) -> list[RetrievedChunk]`
- `propose_action(tenant: TenantContext, proposal: ProposedAction) -> ApprovalRequest`
- `approve_action(request_id: UUID, reviewer: Principal, decision: ApprovalDecision) -> ApprovalResult`
- `execute_approved_action(request_id: UUID, executor: Principal) -> ExecutionResult` — re-check current policy and authorization at execution time.

## Tasks

### 1. Model gateway and benchmark harness
- [ ] Test provider timeout, unavailable provider, invalid output, token limits, cancellation and stable response schema.
- [ ] Implement provider-neutral contract and Ollama development adapter; vLLM only as optional adapter.
- [ ] Benchmark latency, throughput, memory, quality and concurrency on actual target hardware.
- [ ] Do not select production model/quantization before VPS resources and concurrency are measured.
- [ ] Verify tests; commit `feat: add provider independent ai gateway`.

### 2. Safe document ingestion
- [ ] Test oversized files, decompression bombs, malformed PDFs, unsupported MIME, macros, hostile filenames and scanner failures.
- [ ] Implement allowlists, size limits, malware status, isolated parsing/OCR and provenance.
- [ ] Parsers cannot fetch arbitrary URLs or access host filesystem paths.
- [ ] Verify tests; commit `feat: add secure document ingestion`.

### 3. Tenant-scoped retrieval and citations
- [ ] Test cross-tenant retrieval, source allowlists, deleted/expired evidence, duplicates and citation integrity.
- [ ] Implement embeddings and pgvector retrieval with mandatory tenant context and source ACL filters.
- [ ] Require material AI factual claims to cite evidence or be marked unsupported.
- [ ] Verify tests; commit `feat: add tenant scoped retrieval`.

### 4. Prompt-injection and data-leakage defenses
- [ ] Add adversarial fixtures for indirect injection, embedded instructions, retrieved secrets, malicious URLs and cross-tenant exfiltration.
- [ ] Implement untrusted-content delimiting, tool allowlists, output validation, secret redaction and SSRF denial.
- [ ] Verify security tests; commit `security: harden ai document and retrieval boundaries`.

### 5. Privacy Copilot and evaluation
- [ ] Test evidence-gap analysis, policy drafting, vendor summary and remediation recommendations with citation and refusal expectations.
- [ ] Implement versioned prompts and structured output schemas.
- [ ] Build evals for groundedness, citation precision, leakage, refusal correctness and reviewer usefulness.
- [ ] Verify tests/evals; commit `feat: add privacy copilot`.

### 6. Approval and audit integration
- [ ] Test approve/reject, expired approval, changed policy, revoked user, duplicate execution and concurrent execution.
- [ ] Implement approval state machine and execution-time authorization.
- [ ] Record model/version, prompt version, sources, output, reviewer decision and execution result.
- [ ] Verify tests; commit `feat: add human approval and ai audit trail`.

## Exit criteria

- Retrieval is tenant-scoped and source-authorized.
- AI outputs are traceable to model, prompt and evidence.
- Consequential execution requires approval and fresh authorization.
- AI has no unrestricted system or network tools.