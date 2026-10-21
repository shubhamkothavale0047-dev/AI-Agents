"""Optional OpenAI Responses API provider. Uses only the Python standard library."""
import json
import os
import urllib.error
import urllib.request


class AIProviderError(RuntimeError):
    pass


def generate_text(prompt: str, model: str | None = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise AIProviderError(
            "OPENAI_API_KEY environment variable is not set. "
            "Add it to your Render environment variables or local .env file."
        )
    model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    body = {
        "model": model,
        "input": prompt,
        "instructions": (
            "You are the creative strategy engine for ALEX DESIGN STUDIO OS. "
            "Be accurate, practical, licensing-aware, and clearly label assumptions. "
            "Do not claim live research or generated media unless actually performed."
        ),
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")[:1200]
        raise AIProviderError(f"OpenAI API returned HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise AIProviderError(f"Could not reach OpenAI API: {exc.reason}") from exc
    except TimeoutError as exc:
        raise AIProviderError("OpenAI API request timed out.") from exc

    pieces = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text" and part.get("text"):
                    pieces.append(part["text"])
    result = "\n".join(pieces).strip()
    if not result:
        raise AIProviderError("OpenAI response contained no output_text.")
    return result
