# String Nodes

String manipulation utilities for ComfyUI.

## Nodes

| File | Node | Purpose |
|------|------|---------|
| `string_join.py` | StringJoin | Join strings with separator |
| `string_replace.py` | StringReplace | Replace substrings |

## Category

All nodes: `CATEGORY = "Sinyuk/String"`

## StringJoin

Joins multiple strings with optional list input:
- Required: `string_1`, `string_2`, `separator`
- Optional: `string_list` (connected input)
- Filters empty strings when separator provided
- `IS_CHANGED` returns `NaN` for dynamic updates

## Patterns

- Input types defined via TypedDict
- `forceInput: True` for connected inputs
- Empty string defaults for optional text
