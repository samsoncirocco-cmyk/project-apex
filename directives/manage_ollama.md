# Directive: Manage Ollama

## Goal

Manage local LLM inference via Ollama container within the Apex stack.

## Inputs

- Ollama container running in apex-net
- Models stored in Docker volume `ollama-data`

## Tools/Scripts to Use

- Docker exec into Ollama container
- Ollama CLI commands

## Process

### 1. Check Ollama Status

```bash
ssh macpro "docker exec apex-ollama-1 ollama --version"
ssh macpro "docker exec apex-ollama-1 ollama list"
```

**Expected**: Version displayed, list of installed models

### 2. Download New Model

```bash
# Pull a model (runs inside container)
ssh macpro "docker exec apex-ollama-1 ollama pull llama3.2"
ssh macpro "docker exec apex-ollama-1 ollama pull codellama"
ssh macpro "docker exec apex-ollama-1 ollama pull nomic-embed-text"
```

**Expected**: Model downloads and becomes available

### 3. Verify Model Works

```bash
ssh macpro "docker exec apex-ollama-1 ollama run llama3.2 'Say hello in one word'"
```

**Expected**: Returns response from model

### 4. API Access (From Other Containers)

Other containers access Ollama via internal network:

```bash
# From inside any apex container
curl http://ollama:11434/api/generate -d '{"model": "llama3.2", "prompt": "Hello"}'
```

## Model Recommendations

| Model | Size | Purpose |
|-------|------|---------|
| `llama3.2` | 3.8GB | General chat, reasoning |
| `codellama` | 3.8GB | Code generation/review |
| `nomic-embed-text` | 274MB | Text embeddings |
| `llama3.2:1b` | 1.3GB | Lighter alternative |

## Resource Management

### Check Memory Usage

```bash
ssh macpro "docker stats apex-ollama-1 --no-stream"
```

### Limit Concurrent Requests

Ollama processes one request at a time by default. For high load:

```bash
# Set in docker-compose.yml environment
OLLAMA_NUM_PARALLEL=2
```

### GPU Support (Future)

Mac Pro 6,1 has AMD GPU - not supported by Ollama. CPU inference only.

## Outputs

- Models available for inference
- API accessible at `http://ollama:11434` within apex-net

## Edge Cases

**Model download fails:**

```bash
# Check disk space
ssh macpro "df -h"
# Check container logs
ssh macpro "docker logs apex-ollama-1"
```

**Out of memory during inference:**

```bash
# Use smaller model
ssh macpro "docker exec apex-ollama-1 ollama pull llama3.2:1b"
```

**Slow responses:**

- Expected: CPU inference is slower than GPU
- Typical response: 5-30 seconds for 100 tokens
- Consider lighter models for faster response

## Timing

- Model download: 5-30 minutes (depends on size/network)
- Inference: 5-30 seconds per response
- Container restart: ~10 seconds

## Notes

- Models persist in Docker volume (survive container restarts)
- Memory limit set to 8GB in docker-compose.yml
- Other containers access via service name `ollama`
- Consider downloading models during off-hours (bandwidth)
