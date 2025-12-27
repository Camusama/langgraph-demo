from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from langchain.chat_models import init_chat_model

# 默认配置
DEFAULT_MODEL = "deepseek/deepseek-v3.2-exp"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


def _load_env() -> None:
    """从仓库根目录的 .env 加载简单的 KEY=VALUE（无需额外依赖）。"""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_openrouter_model(*, temperature: float = 0, **kwargs: Any):
    """返回一个预配置好的 OpenRouter ChatModel。

    依赖 .env 中的 OPENROUTER_API_KEY，可选 OPENROUTER_BASE_URL 覆盖默认 base_url。
    其他参数可通过 kwargs 传入（如 max_tokens、stop 等）。
    """
    _load_env()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 未设置，请在仓库根目录 .env 中填写。")

    base_url = os.environ.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL)

    return init_chat_model(
        DEFAULT_MODEL,
        model_provider="openai",  # OpenRouter 走 OpenAI 兼容协议
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        **kwargs,
    )
