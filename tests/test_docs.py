import pytest
import ollama

from data.gibberish.docs import create_prompt, DOMAINS, MODEL

@pytest.mark.asyncio
async def test_create_prompt():
    domain = "redsolocup"
    response = f"write me a 500 word IT document based on {domain} in a markdown format and use nonsense words where ever possible"
    prompt = await create_prompt(domain)
    assert prompt == response

def test_domains_list_items():
    domains = DOMAINS
    assert 'encryption' in domains
    assert type(domains) is list

def test_model_name():
    model_name = MODEL
    assert model_name == "mistral:latest"