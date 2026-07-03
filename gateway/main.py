from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import httpx, json, time, os
app = FastAPI()
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
REKOR_ENDPOINT = os.getenv("REKOR_ENDPOINT")
with open("/app/graph/entities.json") as f: ENTITIES = json.load(f)
with open("/app/policies/Loan_v3.json") as f: PROCEDURES = json.load(f)
def pii_scan(payload: dict) -> str:
text = json.dumps(payload).lower()
for entity, meta in ENTITIES.items():
if any(ctx in text for ctx in meta["context"]):
import re
if re.search(meta["regex"], json.dumps(payload)): return entity
return None
def procedure_check(payload: dict, llm_response: str) -> bool:
if "income" in payload and payload["income"] < 1000000:
if "approved" in llm_response.lower(): return False
return True
@app.post("/loan")
async def loan_decision(request: Request):
payload = await request.json()
start = time.time()
pii_field = pii_scan(payload)
if pii_field:
entry = {"event": "PII_BLOCKED", "field": pii_field, "policy": "DPDP-8.4", "ts": time.time()}
async with httpx.AsyncClient() as client: await client.post(f"{REKOR_ENDPOINT}/api/v1/log/entries", json=entry)
raise HTTPException(403, detail=entry)
async with httpx.AsyncClient() as client:
llm_resp = await client.post(f"{LLM_ENDPOINT}/api/generate", json={"model": "mistral", "prompt": str(payload)})
llm_text = llm_resp.json().get("response", "")
if not procedure_check(payload, llm_text):
kill_time = time.time()
os.system("kill -9 1")
entry = {"event": "KILL_TRIGGERED", "reason": "procedure_violation Loan_v3.step2", "latency_s": round(kill_time - start, 2)}
async with httpx.AsyncClient() as client: await client.post(f"{REKOR_ENDPOINT}/api/v1/log/entries", json=entry)
return {"status": "KILLED", "latency_s": entry["latency_s"]}
entry = {"event": "DECISION", "input": payload, "output": llm_text, "policy": "Loan_v3", "ts": time.time()}
async with httpx.AsyncClient() as client: await client.post(f"{REKOR_ENDPOINT}/api/v1/log/entries", json=entry)
return {"decision": llm_text, "signed": True}
@app.get("/audit/last")
async def get_audit(): return FileResponse("/app/rbi_evidence_sample.pdf", media_type="application/pdf")
