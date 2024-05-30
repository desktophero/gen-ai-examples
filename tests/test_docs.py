import pytest

from data.gibberish.docs import create_prompt, DOMAINS, MODEL

@pytest.mark.asyncio
async def test_create_prompt():
    """
    test generating a prompt based on a domain being submitted
    """
    domain = "redsolocup"
    response = f"write me a 500 word IT document based on {domain} in a markdown format and use nonsense words where ever possible"
    prompt = await create_prompt(domain)
    assert prompt == response

def test_domains_list_items():
    """
    test that the DOMAINS list has some sort of specific string
    """
    domains = DOMAINS
    assert 'encryption' in domains
    assert type(domains) is list

def test_model_name():
    """
    verify the model name we're using is defined in the constant value
    """
    model_name = MODEL
    assert model_name == "mistral:latest"