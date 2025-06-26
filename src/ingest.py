import asyncio
import json
import re
from pathlib import Path

MAX_CHUNK_SIZE = 2048  # bytes

async def _read_file_async(path: str) -> str:
    """Read file contents asynchronously using a thread."""
    return await asyncio.to_thread(Path(path).read_text, encoding="utf-8")

async def ingest(path: str) -> list[str]:
    """Load a file and return cleaned 2 kB chunks."""
    raw = await _read_file_async(path)
    # If JSON, pretty-print or extract value
    if path.endswith(".json"):
        try:
            obj = json.loads(raw)
            if isinstance(obj, str):
                raw = obj
            else:
                raw = json.dumps(obj, indent=2)
        except json.JSONDecodeError:
            pass

    text = _strip_markdown(raw)
    return _chunk_text(text)


def _strip_markdown(text: str) -> str:
    """Remove a subset of markdown markup from text."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # code blocks
    text = re.sub(r"`", "", text)  # inline code
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # links
    text = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", text)  # images
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # italics
    text = re.sub(r"^#+", "", text, flags=re.M)  # headings
    return text


def _chunk_text(text: str) -> list[str]:
    """Chunk text into 2 kB segments."""
    data = text.encode("utf-8")
    chunks = []
    start = 0
    while start < len(data):
        end = start + MAX_CHUNK_SIZE
        chunk = data[start:end].decode("utf-8", errors="ignore")
        chunks.append(chunk)
        start = end
    return chunks


__all__ = ["ingest"]