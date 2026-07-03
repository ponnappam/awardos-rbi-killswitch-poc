# Architecture Deep Dive

## Kill Switch Sequence
1. **Request**: Banking app POST /loan
2. **Policy**: Gateway checks RBI rules: income, velocity, KG patterns
3. **Breach**: If violated, start timer
4. **Kill**: `kubectl delete pod` or `docker stop` via control plane
5. **Audit**: POST to Rekor: {event, latency_s, model_hash, hsm_key_id}
6. **Response**: 200 OK with compliance fields

## Why Docker Socket in POC = K8s RBAC in Prod
Both are "control plane access". POC proves the logic. SUSE Rancher makes it enterprise-safe with RBAC, admission control, and FIPS crypto.

## Hardware Scaling
| Workload | POC | SUSE + H100 |
| --- | --- | --- |
| LLM TPS | 2 | 10,000 |
| Kill Latency | 0.85s | 1.4s |
| Nodes | 1 | 50 |
| Data Egress | None | None - Air-gapped |
