
"""RAG-based curation pipeline (orchestrator)."""

import logging, json, pathlib
from typing import List, Dict
from .utils import setup_logging, parse_pdf
from .kg_interface import search_entities, get_entity_info
from .llm_interface import generate_text

logger = logging.getLogger(__name__)
setup_logging()

def find_similar_documents(text: str) -> List[str]:
    # placeholder: returns keyword matches
    return [line.strip() for line in text.split('\n') if 'CO2' in line][:3]

def retrieve_external_knowledge(text: str) -> Dict[str, str]:
    entities = set()
    for line in text.split():
        if line.upper() in ('CO2', 'ESG', 'CSR'):
            entities.add(line.upper())
    facts = {e: get_entity_info(e) for e in entities}
    return facts

def generate_summary(text: str) -> str:
    prompt = f'Summarize in 100 words:\n{text[:2000]}'
    return generate_text(prompt)

def generate_tags(text: str) -> List[str]:
    prompt = f'Extract 5 key ESG tags:\n{text[:2000]}'
    tags_json = generate_text(prompt)
    try:
        tags = json.loads(tags_json)
    except json.JSONDecodeError:
        tags = ['ESG']
    return tags

def run_curation_pipeline(pdf_path: str) -> Dict:
    logger.info(f'Running curation pipeline on {pdf_path}')
    text = parse_pdf(pdf_path)
    similar = find_similar_documents(text)
    facts = retrieve_external_knowledge(text)
    summary = generate_summary(text)
    tags = generate_tags(text)
    result = {
        'source_file': pathlib.Path(pdf_path).name,
        'summary': summary,
        'tags': tags,
        'facts': facts,
        'related_docs_snippets': similar
    }
    out_dir = pathlib.Path('outputs')
    out_dir.mkdir(exist_ok=True)
    out_json = out_dir / (pathlib.Path(pdf_path).stem + '_metadata.json')
    json.dump(result, out_json.open('w'), indent=2)
    logger.info(f'Metadata saved -> {out_json}')
    return result

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python -m active_archives.rag_curation <report.pdf>')
        sys.exit(1)
    run_curation_pipeline(sys.argv[1])
