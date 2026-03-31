# IO Nodes

File and image I/O utilities for ComfyUI.

## Structure

| File | Node | Purpose |
|------|------|---------|
| `save_text.py` | SaveText | Write text with multiple modes |
| `file_exists.py` | FileExists | Check file existence |
| `load_image_by_path.py` | LoadImageByPath | Load single image |
| `load_images_from_folder.py` | LoadImagesFromFolder | Batch image loading |
| `auto_tile_factors.py` | AutoTileFactors | Calculate tile splits |

## Category

All nodes: `CATEGORY = "Sinyuk/IO"`

## SaveText Features

- Write modes: `overwrite`, `append`, `skip`, `new_only`
- Newline modes (append): `none`, `before`, `after`
- Auto-creates directories
- Custom encoding support
- Returns: `(file_path, filename)`

## Patterns

- Use `pathlib.Path` for all path operations
- `OUTPUT_NODE = True` for side-effect nodes
- Descriptive tooltips on all inputs

## Testing

Tests in `tests/test_io_nodes.py`:
- All write modes
- Directory creation
- Encoding handling
- INPUT_TYPES structure validation
