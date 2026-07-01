import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_claude() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def ask(prompt: str, system: str = "") -> str:
    client = get_claude()
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
