
"""Placeholder Knowledge Graph interface (DBpedia / Wikidata)."""

import logging

logger = logging.getLogger(__name__)

MOCK_ENTITIES = {
    'ESG': 'Environmental, Social, and Governance is a framework for...',
    'CO2': 'Carbon dioxide, a greenhouse gas.',
    'Scope 1': 'Direct GHG emissions from owned or controlled sources.'
}

MOCK_RELATED = {
    'ESG': ['CSR', 'sustainability'],
    'CO2': ['greenhouse gas', 'emissions']
}

def search_entities(query: str):
    logger.info(f'Searching KG for "{query}"')
    for k in MOCK_ENTITIES:
        if k.lower() in query.lower():
            yield k

def get_entity_info(entity: str) -> str:
    logger.info(f'Fetching KG info for {entity}')
    return MOCK_ENTITIES.get(entity, '')

def get_related_entities(entity: str):
    return MOCK_RELATED.get(entity, [])
