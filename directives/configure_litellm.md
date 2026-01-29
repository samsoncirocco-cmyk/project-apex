# Directive: Configure LiteLLM Router

## Goal

Configure and manage LiteLLM proxy for unified AI model access across all bot services.

## Inputs

- LiteLLM container running in apex-net
- Ollama container with models downloaded
- Configuration at `~/apex/config/litellm_config.yaml`

## Tools/Scripts to Use

- Docker exec into LiteLLM container
- LiteLLM config file modifications
- curl for API testing

## Process

### 1. Check LiteLLM Status

```bash
ssh macpro "docker logs apex-litellm --tail 20"
ssh macpro "curl -s http://localhost:4000/health | jq"
```

**Expected**: Health check returns `{"status": "healthy"}`

### 2. List Available Models

```bash
ssh macpro "curl -s http://localhost:4000/v1/models | jq '.data[].id'"
```

**Expected**: Lists configured model aliases (gpt-4, gpt-3.5-turbo, etc.)

### 3. Test Chat Completion

```bash
ssh macpro 'curl -s http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"gpt-4\", \"messages\": [{\"role\": \"user\", \"content\": \"Say hello\"}]}" | jq'
```

**Expected**: Returns completion from Ollama llama3.2

### 4. Test Embeddings

```bash
ssh macpro 'curl -s http://localhost:4000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"text-embedding-ada-002\", \"input\": \"Hello world\"}" | jq'
```

**Expected**: Returns embedding vector from nomic-embed-text

## Adding New Models

### 1. Pull Model in Ollama

```bash
ssh macpro "docker exec apex-ollama ollama pull mistral"
```

### 2. Update LiteLLM Config

```bash
ssh macpro "nano ~/apex/config/litellm_config.yaml"
```

Add to model_list:

```yaml
  - model_name: mistral
    litellm_params:
      model: ollama/mistral
      api_base: http://ollama:11434
```

### 3. Restart LiteLLM

```bash
ssh macpro "docker restart apex-litellm"
```

## Model Alias Reference

| API Model Name | Routes To | Use Case |
|----------------|-----------|----------|
| `gpt-4` | `ollama/llama3.2` | General reasoning |
| `gpt-3.5-turbo` | `ollama/llama3.2:1b` | Fast responses |
| `text-embedding-ada-002` | `ollama/nomic-embed-text` | Embeddings |
| `codellama` | `ollama/codellama` | Code generation |

## Outputs

- LiteLLM proxy running on port 4000
- All bot services can use OpenAI-compatible API
- Request logs available via `docker logs apex-litellm`

## Edge Cases

**LiteLLM won't start:**

```bash
# Check config syntax
ssh macpro "docker logs apex-litellm"
# Validate YAML
ssh macpro "python3 -c 'import yaml; yaml.safe_load(open(\"/home/samson/apex/config/litellm_config.yaml\"))'"
```

**Model not responding:**

```bash
# Check Ollama has the model
ssh macpro "docker exec apex-ollama ollama list"
# Check Ollama is healthy
ssh macpro "docker exec apex-ollama curl -s http://localhost:11434/"
```

**Slow responses:**

- Expected: Local CPU inference is 5-30 seconds
- Use smaller models for faster response
- Check system resources: `docker stats`

## Timing

- Container startup: ~10 seconds
- Config reload: ~5 seconds (requires restart)
- First request after model cold start: 10-30 seconds
- Subsequent requests: 5-20 seconds

## Notes

- LiteLLM provides OpenAI-compatible API
- Bot code uses standard OpenAI SDK syntax
- Model routing handled by config, not code
- Master key is optional but recommended for production
