"""
Kimi Chat node - Call Kimi K2.5 model via Moonshot AI API.

Supports:
- Multiple Kimi models (kimi-k2.5, kimi-k2-turbo-preview, moonshot-v1 series)
- System prompt customization
- Temperature and other generation parameters
- Automatic API key loading from environment variable MOONSHOT_API_KEY
- Thinking mode control for kimi-k2.5
"""

from __future__ import annotations

import os
from typing import ClassVar, TypedDict


class InputTypeOptions(TypedDict, total=False):
    """Input type configuration options."""

    default: int | float | str | bool
    min: int | float
    max: int | float
    step: int | float
    display: str
    multiline: bool
    placeholder: str
    forceInput: bool
    tooltip: str


class ComboOptions(TypedDict, total=False):
    """Combo/dropdown type options."""

    default: str
    tooltip: str


class InputTypeDict(TypedDict, total=False):
    """INPUT_TYPES return type."""

    required: dict[
        str,
        tuple[str, InputTypeOptions]
        | tuple[str]
        | tuple[list[str]]
        | tuple[list[str], ComboOptions],
    ]
    optional: dict[
        str,
        tuple[str, InputTypeOptions]
        | tuple[str]
        | tuple[list[str]]
        | tuple[list[str], ComboOptions],
    ]
    hidden: dict[str, str]


# Available Kimi models with descriptions
KIMI_MODELS = [
    "kimi-k2.5",              # 最新旗舰模型，支持思考模式
    "kimi-k2-turbo-preview",  # 高性价比模型，速度快
    "kimi-k2-0905-preview",   # K2 稳定版
    "kimi-k2-0711-preview",   # K2 早期版本
    "kimi-k2-thinking-turbo", # 思考模型 Turbo 版
    "kimi-k2-thinking",       # 思考模型
    "moonshot-v1-8k",         # 8K 上下文
    "moonshot-v1-32k",        # 32K 上下文
    "moonshot-v1-128k",       # 128K 上下文（长文本）
    "moonshot-v1-auto",       # 自动选择上下文长度
]

# Default system prompt - professional and helpful
DEFAULT_SYSTEM_PROMPT = """你是 Kimi，由 Moonshot AI 提供的人工智能助手。你具备以下特点：
- 擅长中文和英文的对话
- 提供安全、有帮助、准确的回答
- 拒绝涉及恐怖主义、种族歧视、黄色暴力等问题
- 回答简洁明了，逻辑清晰"""


class KimiChat:
    """
    调用 Kimi K2.5 模型的 ComfyUI 节点。

    通过 Moonshot AI 的 OpenAI 兼容 API 与 Kimi 模型交互。
    API Key 可以直接输入或从环境变量 MOONSHOT_API_KEY 自动读取。
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "INT", "INT", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = (
        "response",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
    )
    OUTPUT_TOOLTIPS: ClassVar[tuple[str, ...]] = (
        "Kimi 模型的回复文本",
        "输入消息消耗的 token 数量",
        "生成回复消耗的 token 数量",
        "总共消耗的 token 数量（用于计费）",
    )
    FUNCTION: ClassVar[str] = "execute"
    CATEGORY: ClassVar[str] = "Sinyuk/LLM"
    DESCRIPTION: ClassVar[str] = "调用 Kimi K2.5 大模型进行对话，支持多种模型和思考模式"
    OUTPUT_NODE: ClassVar[bool] = False

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {
                        "default": "你好，请介绍一下你自己",
                        "multiline": True,
                        "placeholder": "在这里输入你的问题或指令...",
                        "tooltip": "发送给 Kimi 的用户消息。支持多行文本，可以输入复杂的问题或指令。",
                    },
                ),
                "model": (
                    KIMI_MODELS,
                    {
                        "default": "kimi-k2.5",
                        "tooltip": "选择 Kimi 模型：\n• kimi-k2.5：最新旗舰模型，支持深度思考\n• kimi-k2-turbo-preview：高性价比，响应更快\n• moonshot-v1-128k：支持超长上下文（128K tokens）",
                    },
                ),
            },
            "optional": {
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": "留空则自动读取 MOONSHOT_API_KEY 环境变量",
                        "tooltip": "Moonshot API Key。获取方式：访问 platform.moonshot.cn 注册并创建 API Key。\n\n推荐使用环境变量 MOONSHOT_API_KEY 存储，更安全。",
                    },
                ),
                "system_prompt": (
                    "STRING",
                    {
                        "default": DEFAULT_SYSTEM_PROMPT,
                        "multiline": True,
                        "placeholder": "设置 AI 助手的行为和角色...",
                        "tooltip": "系统提示词，用于设定 Kimi 的角色、行为和回答风格。\n\n例如：\n• '你是一个专业的翻译助手'\n• '你是一个 Python 编程专家'\n• '请用简洁的语言回答问题'",
                    },
                ),
                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.6,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.05,
                        "display": "slider",
                        "tooltip": "采样温度，控制回复的随机性：\n• 0.0-0.3：更确定、更一致的回答（适合代码、翻译）\n• 0.4-0.7：平衡创意和准确性（推荐值：0.6）\n• 0.8-1.0：更有创意、更多样化（适合写作、头脑风暴）\n\n注意：kimi-k2.5 思考模式固定为 1.0",
                    },
                ),
                "max_tokens": (
                    "INT",
                    {
                        "default": 4096,
                        "min": 64,
                        "max": 32768,
                        "step": 64,
                        "tooltip": "最大生成 token 数量，限制回复的长度：\n• 256-512：简短回答\n• 1024-2048：中等长度回答\n• 4096+：详细回答或长文本生成\n\n1 个中文字符约等于 1-2 个 tokens",
                    },
                ),
                "enable_thinking": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "启用思考模式（仅对 kimi-k2.5 生效）。\n\n开启后，模型会先进行深度思考再回答，适合：\n• 复杂推理问题\n• 数学计算\n• 代码编写\n• 多步骤任务\n\n关闭后响应更快，适合简单问答。",
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 0.95,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.05,
                        "display": "slider",
                        "tooltip": "Top-p 核采样参数：\n• 控制从概率最高的 tokens 中采样的范围\n• 0.95 表示从累计概率 95% 的 tokens 中采样\n• 较低值使输出更集中，较高值增加多样性\n\n一般保持默认值 0.95 即可，通常调整 temperature 更直观。\n\n注意：kimi-k2.5 固定为 0.95",
                    },
                ),
            },
        }

    @classmethod
    def IS_CHANGED(
        cls,
        prompt: str,
        model: str,
        api_key: str = "",
        system_prompt: str = "",
        temperature: float = 0.6,
        max_tokens: int = 4096,
        enable_thinking: bool = True,
        top_p: float = 0.95,
    ) -> float:
        """Always re-execute to get fresh responses."""
        return float("nan")

    def execute(
        self,
        prompt: str,
        model: str,
        api_key: str = "",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        temperature: float = 0.6,
        max_tokens: int = 4096,
        enable_thinking: bool = True,
        top_p: float = 0.95,
    ) -> tuple[str, int, int, int]:
        """
        调用 Kimi API 并返回响应。

        Args:
            prompt: 用户消息
            model: Kimi 模型名称
            api_key: API Key（留空则从环境变量读取）
            system_prompt: 系统提示词
            temperature: 采样温度
            max_tokens: 最大生成 token 数
            enable_thinking: 启用思考模式（仅 kimi-k2.5）
            top_p: Top-p 采样参数

        Returns:
            (回复文本, 输入tokens, 输出tokens, 总tokens)
        """
        # Import OpenAI client here to avoid startup overhead
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "需要安装 OpenAI 包。请运行：pip install 'openai>=1.0'"
            ) from e

        # Get API key from parameter or environment
        actual_api_key = api_key.strip() if api_key else os.environ.get("MOONSHOT_API_KEY", "")

        if not actual_api_key:
            raise ValueError(
                "需要提供 API Key。请直接输入，或设置环境变量 MOONSHOT_API_KEY。\n"
                "获取 API Key：https://platform.moonshot.cn/"
            )

        # Create OpenAI client with Moonshot China base URL
        client = OpenAI(
            api_key=actual_api_key,
            base_url="https://api.moonshot.cn/v1",
        )

        # Build messages
        messages: list[dict[str, str]] = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Build request parameters
        request_params: dict[str, object] = {
            "model": model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
        }

        # Handle kimi-k2.5 specific parameters
        # Use extra_body for Kimi-specific parameters that OpenAI SDK doesn't recognize
        extra_body: dict[str, object] = {}

        if model == "kimi-k2.5":
            # kimi-k2.5 has fixed temperature and top_p values based on thinking mode
            if enable_thinking:
                extra_body["thinking"] = {"type": "enabled"}
                # temperature is fixed at 1.0 for thinking mode
            else:
                extra_body["thinking"] = {"type": "disabled"}
                # temperature is fixed at 0.6 for non-thinking mode
            # top_p is fixed at 0.95 for kimi-k2.5
        else:
            # Other models can customize temperature and top_p
            request_params["temperature"] = temperature
            request_params["top_p"] = top_p

        # Add extra_body if there are Kimi-specific parameters
        if extra_body:
            request_params["extra_body"] = extra_body

        # Make the API call
        try:
            completion = client.chat.completions.create(**request_params)  # type: ignore[arg-type]
        except Exception as e:
            error_msg = str(e)
            if "invalid_authentication_error" in error_msg or "incorrect_api_key" in error_msg:
                raise RuntimeError("API Key 无效，请检查是否正确。") from e
            elif "exceeded_current_quota" in error_msg:
                raise RuntimeError("账户余额不足，请充值后重试。") from e
            elif "rate_limit" in error_msg:
                raise RuntimeError("请求频率超限，请稍后重试。") from e
            elif "content_filter" in error_msg:
                raise RuntimeError("内容审查拒绝，请修改输入内容。") from e
            else:
                raise RuntimeError(f"Kimi API 调用失败：{e}") from e

        # Extract response
        choice = completion.choices[0]
        response_text: str = choice.message.content if choice.message.content else ""

        # Extract token usage
        usage = completion.usage
        prompt_tokens: int = usage.prompt_tokens if usage else 0
        completion_tokens: int = usage.completion_tokens if usage else 0
        total_tokens: int = usage.total_tokens if usage else 0

        return (response_text, prompt_tokens, completion_tokens, total_tokens)


NODE_CLASS_MAPPINGS = {
    "Sinyuk_KimiChat": KimiChat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sinyuk_KimiChat": "Kimi Chat (K2.5)",
}