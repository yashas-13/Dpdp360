# DPDP360

AI-assisted DPDP compliance and privacy-operations platform for Indian organizations.

**Product owner:** Pravidhi Tech Solutions LLP  
**Repository:** https://github.com/yashas-13/Dpdp360  
**Status:** Approved design and implementation planning; application implementation has not started.

## Product direction

DPDP360 supports organizations from SMEs through enterprise with readiness assessments and continuous privacy operations. Planned capabilities include compliance controls, evidence, remediation, personal-data inventory, processing activities, consent and notices, Data Principal request workflows, vendor/processor management, breach workflows, and an AI Privacy Copilot.

## Approved architecture

- Multi-tenant SaaS plus dedicated enterprise private deployment.
- Separate PostgreSQL database and credentials for each SaaS tenant.
- Server-side tenant resolution; never trust browser-supplied tenant IDs or DB connection strings.
- Modular monolith initially, with independently deployable workers.
- Next.js + TypeScript web application; Python FastAPI API; PostgreSQL, Redis, Celery, pgvector and S3-compatible object storage.
- Provider-independent AI gateway using self-hosted open-source models. Ollama is a development candidate; vLLM is a production candidate subject to benchmark.
- Initial hosting on Pravidhi infrastructure with cloud-ready deployment design.

## Ownership and governance

All product IP, source code, architecture, infrastructure, deployment, operations, customer relationships, support, sales and commercialization belong to **Pravidhi Tech Solutions LLP**. VarnueAI is not a co-owner or delivery owner; it may only be an optional technology vendor or integration provider.

AI can analyze, recommend and draft. Consequential actions require human approval and server-side policy authorization. AI is never the authorization authority. Regulatory mappings must retain authoritative source, effective date, applicability and supersession history, and require qualified legal review before production use. DPDP360 supports compliance operations; it does not provide legal advice or guarantee compliance. Do not claim Consent Manager registration/status unless applicable requirements are met.

## Planning documents

- [Approved design specification v1.0](docs/superpowers/specs/2026-11-20-dpdp360-design-spec-v1.md)
- [Platform foundation plan](docs/superpowers/plans/2026-11-20-dpdp360-platform-foundation.md)
- [Compliance engine plan](docs/superpowers/plans/2026-11-20-dpdp360-compliance-engine.md)
- [Privacy operations plan](docs/superpowers/plans/2026-11-20-dpdp360-privacy-operations.md)
- [AI intelligence plan](docs/superpowers/plans/2026-11-20-dpdp360-ai-intelligence.md)
- [Enterprise operations plan](docs/superpowers/plans/2026-11-20-dpdp360-enterprise-operations.md)

## Execution order

Foundation → Compliance Engine → Privacy Operations → AI Intelligence → Enterprise Operations.

Implementation is gated on isolated workspaces, test-first changes, focused review after each task, tenant-isolation security tests, and a final integration/security review. Production regulatory mappings require qualified legal approval.

## Public repository notice

This repository is currently public at the owner's direction. Do not commit secrets, credentials, customer data, personal data, private infrastructure details, or sensitive operational runbooks. Consider switching visibility to private before adding proprietary implementation details.
