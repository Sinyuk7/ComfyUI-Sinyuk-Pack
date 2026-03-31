# ComfyUI-Sinyuk-Pack

A personal collection of custom nodes for ComfyUI with pytest support.

## Structure

```
.
├── nodes/           # Node implementations
│   ├── io/         # File I/O utilities
│   ├── strings/    # String manipulation
│   └── llm/        # LLM API integrations
├── tests/          # pytest suite
├── comfy_types.py  # Type definitions for strict checking
└── openspec/       # Spec-driven dev config
```

## Entry Points

| File | Purpose |
|------|---------|
| `__init__.py` | Aggregates all node mappings for ComfyUI |
| `nodes/<cat>/__init__.py` | Per-category node exports |

## Node Registration

Each node module exports:
- `NODE_CLASS_MAPPINGS`: Dict[str, type] - Class registration
- `NODE_DISPLAY_NAME_MAPPINGS`: Dict[str, str] - UI display names

Category prefix: `Sinyuk_*` (e.g., `Sinyuk_SaveText`)

## Node Structure

Required class attributes:
```python
RETURN_TYPES: ClassVar[tuple[str, ...]]     # Output types
RETURN_NAMES: ClassVar[tuple[str, ...]]     # Output names
FUNCTION: ClassVar[str]                     # Execute method name
CATEGORY: ClassVar[str]                     # UI category
```

Required methods:
```python
@classmethod
def INPUT_TYPES(cls) -> InputTypeDict: ...

def execute(self, ...) -> tuple: ...
```

## Dual Environment Support

All `__init__.py` files use conditional imports:
```python
try:
    from .module import Class  # ComfyUI (relative)
except ImportError:
    from nodes.module import Class  # pytest (absolute)
```

## Type Checking

- `comfy_types.py`: TypedDict definitions for INPUT_TYPES
- `pyproject.toml`: Pyright strict mode enabled
- Python 3.11+ type syntax required

## Commands

```bash
# Run tests
pytest

# Type check
pyright
```

## Conventions

- Chinese comments allowed for internal notes
- `__future__.annotations` required in all files
- `ClassVar` for class-level type annotations
- Tooltip descriptions on all input fields

## Anti-Patterns

- Do NOT use bare `dict` - use `dict[str, ...]`
- Do NOT use `typing` imports when `collections.abc` equivalents exist
- Always include `from __future__ import annotations`
