# AwardOS SUSE RBI Demo - Ollama Gateway

OpenAI-compatible gateway for Ollama running `llama3.2:1b`. Built for low-RAM demos.

## Architecture
```
Client -> Flask Gateway :8443 -> Ollama :11434 -> llama3.2:1b
```

## Prerequisites
- Docker + Docker Compose
- 4GB RAM minimum, 8GB recommended
- Ports 8443 and 11434 free

## Quick Start

**1. Clone and start:**
```bash
git clone <your-repo-url>
cd awardos-suse-rbi-demo
docker compose up -d
```

**2. Wait for model pull:**
```bash
docker compose logs -f balk-llm
```

**3. Test:**
```bash
curl http://localhost:8443/v1/models
```
