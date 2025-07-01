
"""RAG‑based metadata curation pipeline (compact educational version).

Architecture mapping (paper Section 3.2):
  1. ingest_document()                 →  New Document Input
  2. retrieve_internal_passages()      →  Retriever (Internal)
  3. retrieve_external_kg_facts()      →  Retriever (External KG)
  4. build_rag_context()               →  Context Fusion
  5. generate_metadata_with_llm()      →  LLM Generation
  6. curator_review()                  →  Archivist Review
  7. update_metadata_store()           →  KB & Archive Update
This script purposefully keeps an in‑memory workflow while mirroring the logical
steps of the full pipeline. Replace stubs with production integrations as needed.
"""

import re, json, pathlib, uuid, datetime
from typing import List, Dict

# -----------------------------------------------------------------------------
# 1 · Document ingestion
# -----------------------------------------------------------------------------
def ingest_document(pdf_path: str) -> str:
    """Extract raw text from a PDF file (very naive)."""
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    pages_text = [p.extract_text() or '' for p in reader.pages]
    document_text = '\n'.join(pages_text)
    return document_text


# -----------------------------------------------------------------------------
# 2 · Internal semantic retrieval (toy implementation)
# -----------------------------------------------------------------------------
def retrieve_internal_passages(document_text: str, keywords: List[str]) -> List[str]:
    """Return sentences that contain any of the target keywords."""
    sentences = re.split(r'(?<=[.!?])\s+', document_text)
    hits = [
        s for s in sentences
        if any(k.lower() in s.lower() for k in keywords)
    ]
    # keep at most 5 passages
    return hits[:5]


# -----------------------------------------------------------------------------
# 3 · External KG retriever (mock DBpedia look‑ups)
# -----------------------------------------------------------------------------
MOCK_KG = {
    "Scope 1": "Direct greenhouse‑gas emissions that occur from sources controlled by the organisation.",
    "CO2": "A colourless gas consisting of carbon and oxygen atoms; primary greenhouse gas."
}

def retrieve_external_kg_facts(entities: List[str]) -> Dict[str, str]:
    """Return explanatory facts for each entity (stub for DBpedia/Wikidata API)."""
    return {e: MOCK_KG.get(e, '') for e in entities}


# -----------------------------------------------------------------------------
# 4 · Context fusion
# -----------------------------------------------------------------------------
def build_rag_context(passages: List[str], kg_facts: Dict[str, str]) -> str:
    facts_block = '\n'.join(f'* {k}: {v}' for k, v in kg_facts.items() if v)
    passages_block = '\n'.join(passages)
    prompt = f"""You are an ESG archivist assistant.
Context facts:
{facts_block}

Document excerpts:
{passages_block}

Based on the evidence above, extract YEAR, METRIC NAME, and VALUE (with unit).
Return a JSON dictionary with keys: year, metric, value, unit, cited_passage."""
    return prompt


# -----------------------------------------------------------------------------
# 5 · LLM generation (replace with real model)
# -----------------------------------------------------------------------------
def generate_metadata_with_llm(prompt: str) -> Dict:
    """Rule‑based fallback that mimics an LLM returning JSON."""
    # naive heuristics
    year = re.search(r'(20\d{2})', prompt)
    value = re.search(r'(\d+[\.,]?\d*)\s*(?:Mt|t|tonnes)', prompt, re.I)
    return {
        "year": int(year.group(1)) if year else None,
        "metric": "Scope 1 CO₂ Emissions",
        "value": value.group(1) if value else None,
        "unit": "metric tonnes (tCO₂e)",
        "cited_passage": prompt.split('Document excerpts:')[-1].strip().split('\n')[0]
    }


# -----------------------------------------------------------------------------
# 6 · Curator review (interactive or auto‑accept)
# -----------------------------------------------------------------------------
def curator_review(metadata: Dict) -> Dict:
    """Simulate human validation (auto‑approve for demo)."""
    # In a GUI, the curator could edit fields here.
    metadata['curator_approved'] = True
    metadata['curator_timestamp'] = datetime.datetime.utcnow().isoformat()
    return metadata


# -----------------------------------------------------------------------------
# 7 · Update store
# -----------------------------------------------------------------------------
METADATA_STORE = pathlib.Path('outputs/metadata.json')

def update_metadata_store(metadata: Dict, store_path: pathlib.Path = METADATA_STORE) -> None:
    store_path.parent.mkdir(exist_ok=True)
    data = []
    if store_path.exists():
        data = json.load(store_path.open())
    data.append(metadata)
    json.dump(data, store_path.open('w'), indent=2)
    print(f"✓ Metadata appended to {store_path}")


# -----------------------------------------------------------------------------
# Orchestrator
# -----------------------------------------------------------------------------
def curate_document(pdf_file: str) -> None:
    doc_text = ingest_document(pdf_file)
    passages = retrieve_internal_passages(doc_text, keywords=['CO2', 'Scope 1', 'emissions'])
    kg_facts = retrieve_external_kg_facts(['CO2', 'Scope 1'])
    prompt = build_rag_context(passages, kg_facts)
    ai_metadata = generate_metadata_with_llm(prompt)
    vetted = curator_review(ai_metadata)
    update_metadata_store(vetted, METADATA_STORE)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python rag_curation.py <esg_report.pdf>")
        sys.exit(1)
    curate_document(sys.argv[1])
