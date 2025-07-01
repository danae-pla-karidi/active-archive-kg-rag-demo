
"""Placeholder interface for LLM calls (OpenAI, HF, etc.)."""

import logging, json, random

logger = logging.getLogger(__name__)

def generate_text(prompt: str, model: str = 'gpt-4o', **kwargs) -> str:
    logger.info(f'LLM call to {model} with {len(prompt)} chars')
    # placeholder implementation
    if 'summarize' in prompt.lower():
        return 'This is a placeholder summary of the document.'
    elif 'tags' in prompt.lower():
        return json.dumps(['sustainability', 'CO2', 'Scope 1'])
    else:
        return 'LLM response placeholder.'

def chat_completion(messages, model: str = 'gpt-4o', **kwargs):
    # messages: list of {role, content}
    prompt = '\n'.join([m['content'] for m in messages])
    return generate_text(prompt, model=model, **kwargs)
