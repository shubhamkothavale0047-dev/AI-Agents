import os
from .ai_provider import AIProviderError, generate_text


def main():
    previous = os.environ.pop("OPENAI_API_KEY", None)
    try:
        try:
            generate_text("Offline test")
        except AIProviderError as exc:
            assert "OPENAI_API_KEY is missing" in str(exc)
            print("PASS: OpenAI mode safely rejects missing API key.")
        else:
            raise AssertionError("Expected missing-key failure.")
    finally:
        if previous is not None:
            os.environ["OPENAI_API_KEY"] = previous
    print("NOTE: No external API call was made.")


if __name__ == "__main__":
    main()
