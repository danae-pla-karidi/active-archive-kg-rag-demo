
"""Knowledge graph guided exploration pipeline."""

import logging, re, pathlib
from typing import List, Dict
from .kg_interface import search_entities, get_related_entities
from .utils import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

def parse_query(query: str) -> List[str]:
    return re.findall(r'[\w]+', query)

def expand_query(tokens: List[str]) -> List[str]:
    expanded = list(tokens)
    for tok in tokens:
        for ent in search_entities(tok):
            expanded += get_related_entities(ent)
    return list(dict.fromkeys(expanded))

def search_corpus(expanded_terms: List[str], corpus_dir='data') -> Dict[str, str]:
    hits = {}
    for txt in pathlib.Path(corpus_dir).glob('*.txt'):
        content = txt.read_text(encoding='utf-8', errors='ignore')
        for t in expanded_terms:
            if t.lower() in content.lower():
                hits[txt.name] = content[:200] + '...'
                break
    return hits

def run_exploration_pipeline(query: str):
    logger.info(f'Exploration query: "{query}"')
    tokens = parse_query(query)
    expanded = expand_query(tokens)
    hits = search_corpus(expanded)
    logger.info('--- Expanded terms ---')
    logger.info(expanded)
    logger.info('--- Hits ---')
    for f, snippet in hits.items():
        logger.info(f'{f}: {snippet[:120]}')
    return hits

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python -m active_archives.kg_exploration "<query>"')
        sys.exit(1)
    run_exploration_pipeline(sys.argv[1])
