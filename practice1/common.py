"""practice1 通用工具：向量库构建、加载与格式化."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Sequence

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / ".chroma"

SAMPLE_DOCS = {
    "langgraph_notes.md": """
# LangGraph 学习笔记
- LangGraph 使用 StateGraph 构建节点、边与条件分支，可形成循环。
- 状态本身就是内存，常见字段为 messages、turns、context。
- 可用 MemorySaver/SqliteSaver 持久化对话，支持恢复执行。
""",
    "tooling_snippets.md": """
# LangChain 工具提示
- LangChain 1.x 的工具需通过模型 bind_tools，再解析 tool_calls 执行。
- 常见工具：TavilySearchResults（联网）、PythonREPLTool（计算）、RequestsGetTool（拉取网页）。
- 工具返回 ToolMessage，携带 tool_call_id 以便模型继续推理。
""",
    "rag_tips.md": """
# RAG 提示
- 准备文本 -> 切分 -> 嵌入 -> 写入向量库 -> 检索 -> LLM 汇编回答。
- 评价 RAG 时关注命中文档、引用标记、以及检索失败时的兜底提示。
""",
}


def ensure_sample_corpus() -> List[Path]:
    """在 data 目录生成少量示例文档，便于快速运行。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    for filename, content in SAMPLE_DOCS.items():
        path = DATA_DIR / filename
        if not path.exists():
            path.write_text(content.strip() + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def load_documents() -> List[Document]:
    """加载并切分 data 目录中的文档。"""
    ensure_sample_corpus()
    raw_docs: List[Document] = []
    for path in DATA_DIR.glob("*.md"):
        loader = TextLoader(str(path), encoding="utf-8")
        raw_docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    split_docs = splitter.split_documents(raw_docs)
    for doc in split_docs:
        source = doc.metadata.get("source")
        if source:
            doc.metadata["source"] = Path(source).name
    return split_docs


def get_embeddings() -> Embeddings:
    """返回默认的 OpenAIEmbeddings，需设置 OPENAI_API_KEY。"""
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=model)


def build_vectorstore(*, persist: bool = True) -> Chroma:
    """从文档构建 Chroma 向量库。"""
    docs = load_documents()
    embeddings = get_embeddings()
    persist_dir = str(PERSIST_DIR) if persist else None
    return Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_dir
    )


def load_vectorstore(*, persist: bool = True) -> Chroma:
    """加载或构建向量库。"""
    embeddings = get_embeddings()
    if persist and PERSIST_DIR.exists():
        return Chroma(
            persist_directory=str(PERSIST_DIR), embedding_function=embeddings
        )
    return build_vectorstore(persist=persist)


def format_docs(docs: Sequence[Document]) -> str:
    """把检索到的文档转成可读字符串。"""
    chunks = []
    for idx, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        chunks.append(f"[source{idx}:{source}] {doc.page_content}")
    return "\n\n".join(chunks)


def print_hits(query: str, hits: Iterable[tuple[Document, float]]) -> None:
    """调试打印检索结果。"""
    print(f"\n=== Query: {query} ===")
    for rank, (doc, score) in enumerate(hits, 1):
        source = doc.metadata.get("source", "unknown")
        preview = doc.page_content.replace("\n", " ")[:120]
        print(f"{rank}. score={score:.4f} source={source} preview={preview}")
