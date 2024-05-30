import pytest
import ollama

from data.gibberish.docs import create_prompt

@pytest.mark.asyncio
async def test_create_prompt():
    domain = "redsolocup"
    response = f"write me a 500 word IT document based on {domain} in a markdown format and use nonsense words where ever possible"
    prompt = await create_prompt(domain)
    assert prompt == response

