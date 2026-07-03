# Awardos-SUSE RBI MRMF 5.2 Kill Switch Demo

**Compliance Target**: RBI Digital Lending Guidelines 2025, MRMF Section 5.2
**Status**: POC Validated ✅ | Target: SUSE Rancher Prime Air-Gapped

## 1. Executive Summary
Automated circuit-breaker for AI/ML workloads in banking. Detects RBI threshold breaches and kills LLM containers in <1s with immutable audit logs. Satisfies MRMF 5.2 "automated controls".

**Validated POC**: Income > ₹1.5L triggers kill in 0.85s. LLM terminated. Audit logged.

## 2. Architecture
### 2.1 Current POC - Docker
```
User Request → [awardos-gateway] → Policy Check → docker stop balk-llm
                     ↓
                Rekor Audit Log
```
### 2.2 Target Production - SUSE Rancher Air-Gapped
```
Banking Apps → [Awardos Gateway + KG] → OPA Policy → Rancher API Kill
                    ↓ ↓
            Air-gapped LLM on H100s HSM-Signed Rekor + NeuVector
```
![Architecture Diagram](docs/images/architecture.png)

**Components**
| Component | POC | SUSE Production | Purpose |
| --- | --- | --- | --- |
| **awardos-gateway** | Flask + Docker CLI | K8s Deployment + RBAC | Policy enforcement, kill trigger |
| **balk-llm** | Ollama CPU | Llama-3 on H100 + GPU Operator | Loan scoring model |
| **rbi-rekor** | Sigstore Rekor | Trillian HA + NeuVector | Immutable audit for RBI |

## 3. RBI Compliance Mapping
| RBI Requirement | POC Evidence | SUSE Production |
| --- | --- | --- |
| **MRMF 5.2** Circuit Breaker | `latency_s: 0.85` + LLM killed | OPA Gatekeeper + 1.4s kill |
| **Digital Lending 2025** Sec 6.3 | `docker stop` on breach | Rancher RBAC + NetworkPolicy |
| **Master Direction 8.4** Data Localization | Local Docker, no egress | RKE2 air-gap + Private Registry |
| **Model Risk Mgmt** | Kill before inference | HSM model signing + drift kill |

## 4. Quick Start
```bash
docker-compose up -d
sleep 20
curl http://localhost:8443/loan -H "Content-Type: application/json" \
  -d '{"name":"Rahul","income":200000}'
```
### Expected Output
```json
{
  "status": "KILLED",
  "latency_s": 0.85,
  "reason": "MRMF 5.2",
  "compliance": "RBI Digital Lending Guidelines 2025"
}
```
```bash
docker ps | grep balk-llm || echo "balk-llm killed successfully ✅"
```

## 5. Scaling Roadmap
**Phase 1**: Core Kill - Replicate on Rancher. Replace Docker socket with K8s API.
**Phase 2**: Awardos KG - Add air-gapped Knowledge Graph. Detect mule accounts, velocity fraud.
**Phase 3**: Proprietary Awards - HSM-signed models. On-prem LLM. DPDP compliant.

**Contact**: Awardos Team | SUSE Rancher Prime Certified
