"""
Type definitions for ComfyUI nodes.
These types ensure strict type checking with Pylance.
"""

from __future__ import annotations

from typing import TypedDict


class InputTypeOptions(TypedDict, total=False):
    """输入类型的配置选项"""

    default: int | float | str | bool
    min: int | float
    max: int | float
    step: int | float
    display: str
    multiline: bool
    placeholder: str
    forceInput: bool
    lazy: bool
    rawLink: bool
    tooltip: str


class InputTypeDict(TypedDict, total=False):
    """INPUT_TYPES 返回值的类型"""

    required: dict[str, tuple[str, InputTypeOptions] | tuple[str]]
    optional: dict[str, tuple[str, InputTypeOptions] | tuple[str]]
    hidden: dict[str, str]
