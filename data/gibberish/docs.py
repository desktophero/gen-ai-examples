
import asyncio
import json
import ollama
import os

FOLDER = "data/gibberish/output"

DOMAINS = [
    "access control",
    "encryption",
    "third party security",
    "vulnerability management",
    "acceptable use",
    "asset management",
    "data categorization"
]

MODEL = "mistral:latest"

async def write_file(filename: str, data: str) -> bool:
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(data)
        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

async def create_prompt(domain: str) -> str:
    prompt = f"write me a 500 word IT document based on {domain} in a markdown format and use nonsense words where ever possible"
    return prompt

async def send_prompt(prompt: str) -> str:
    response = ollama.chat(
          model=MODEL,
          messages=[
                {
                      "role": "user",
                      "content": prompt
                }
          ]
    )
    return response

if __name__ == "__main__":
    for d in DOMAINS:
        print(f"Creating document for {d}")
        doc_prompt = asyncio.run(create_prompt(d))
        doc_gen = asyncio.run(send_prompt(doc_prompt))
        json_gen = json.loads(json.dumps(doc_gen))
        doc_write = asyncio.run(
            write_file(f"{FOLDER}/{d}.md", json_gen['message']['content'])
        )
