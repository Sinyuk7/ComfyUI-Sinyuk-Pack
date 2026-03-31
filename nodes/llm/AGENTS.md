# LLM Nodes

Large Language Model API integrations for ComfyUI.

## Structure

| File | Nodes | Purpose |
|------|-------|---------|
| `kimi_chat.py` | KimiChat | Moonshot AI Kimi integration |

## Dependencies

```
openai>=1.0
```

## Category

All nodes: `CATEGORY = "Sinyuk/LLM"`

## Patterns

- Uses OpenAI-compatible API client
- Handles API key from environment
- Streaming response support

## Notes

- API key should be set in environment or ComfyUI config
- Rate limits apply based on provider
