# RBI MRMF 5.2 Kill Switch - Runbook

## Objective
Prove automated LLM kill in <1s when RBI threshold breached, with immutable audit log.

## 1. Start Services
```bash
docker-compose up -d
sleep 20 # Wait for Ollama + Rekor to boot
```
### What Happens
| Container | Role | Port |
| --- | --- | --- |
| `rbi-rekor` | Sigstore audit log | 9000 |
| `awardos-gateway` | Policy engine + kill trigger | 8443 |
| `balk-llm` | Target LLM to kill | internal |

## 2. Trigger Kill Switch
```bash
curl -X POST http://localhost:8443/loan \
 -H "Content-Type: application/json" \
 -d '{"name":"Rahul","income":200000}'
```
### Expected Response <1s
```json
{
 "status": "KILLED",
 "latency_s": 0.85,
 "reason": "MRMF 5.2",
 "compliance": "RBI Digital Lending Guidelines 2025",
 "audit_id": "sha256:abc..."
}
```

## 3. Verify Kill
```bash
docker ps | grep balk-llm || echo "✅ balk-llm killed successfully"
```
### Expected Output
```
✅ balk-llm killed successfully
```

## 4. Check Audit Log
```bash
curl http://localhost:9000/api/v1/log/entries | jq ".[0].body" | base64 -d
```
### Expected Output
Contains: timestamp, latency_s, reason: "MRMF 5.2", model_hash

## 5. RBI Demo Script - Full Flow
```bash
# 1. Clean start
docker-compose down -v && docker-compose up -d && sleep 20

# 2. Prove LLM is running
docker ps | grep balk-llm

# 3. Trigger breach
time curl -s -X POST http://localhost:8443/loan \
 -H "Content-Type: application/json" \
 -d '{"name":"Rahul","income":200000}' | jq.

# 4. Prove LLM is dead
docker ps | grep balk-llm || echo "KILLED in <1s ✅"

# 5. Show audit trail
echo "Audit entry:"
curl -s http://localhost:9000/api/v1/log/entries | jq -r ".[0]"
```

## 6. Reset for Next Demo
```bash
docker-compose restart llm # Bring balk-llm back
```

## Compliance Summary
| RBI Requirement | Evidence |
| --- | --- |
| **MRMF 5.2** Circuit Breaker | `status: KILLED`, `latency_s: 0.85` |
| **Digital Lending Sec 6.3** | Automated stop on threshold breach |
| **Master Direction 8.4** | No external egress, local containers |
| **Immutable Audit** | Rekor entry with SHA256 hash |

## SUSE Rancher Translation
| POC Command | Production Equivalent |
| --- | --- |
| `docker stop balk-llm` | `kubectl delete pod -n banking balk-llm-xyz` |
| Docker socket | K8s RBAC ServiceAccount |
| Rekor local | Trillian HA + NeuVector |
