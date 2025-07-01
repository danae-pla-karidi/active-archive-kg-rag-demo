
"""Knowledge‑graph‑guided exploration prototype.

Architecture mapping (paper Section 3.1):
  1. parse_query()               →  NLP Parser
  2. link_entities_to_kg()       →  Entity Linking to KG
  3. expand_query_terms()        →  Keyword Expansion
  4. retrieve_documents()        →  KB / Graph Retriever + Index Search
  5. rank_results()              →  Result Scoring
  6. build_semantic_subgraph()   →  Semantic Subgraph Generator
  7. display_results()           →  Result Viewer

"""

import re, json, pathlib, networkx as nx
from typing import List, Dict, Tuple

# ----------------------------------------------------------------------
# 1 · NLP query parse 
# ----------------------------------------------------------------------
def parse_query(q: str) -> List[str]:
    tokens = re.findall(r"[\w']+", q)
    return tokens


# ----------------------------------------------------------------------
# 2 · Entity linking (map keywords to mock DBpedia IDs)
# ----------------------------------------------------------------------
KG_ENTITIES = {
    'CO2': 'dbr:Carbon_dioxide',
    'emissions': 'dbr:Greenhouse_gas',
    'Scope': 'dbr:Greenhouse_gas_protocol'
}

def link_entities_to_kg(tokens: List[str]) -> Dict[str, str]:
    return {t: KG_ENTITIES[t] for t in tokens if t in KG_ENTITIES}


# ----------------------------------------------------------------------
# 3 · Keyword expansion
# ----------------------------------------------------------------------
EXPANSION = {
    'CO2': ['carbon dioxide', 'CO₂', 'greenhouse gas'],
    'emissions': ['footprint', 'GHG', 'discharge']
}

def expand_query_terms(entities: Dict[str, str]) -> List[str]:
    expanded = []
    for t in entities:
        expanded += EXPANSION.get(t, [])
    return expanded


# ----------------------------------------------------------------------
# 4 · Retrieve documents (scan local ESG PDFs converted to txt)
# ----------------------------------------------------------------------
def retrieve_documents(terms: List[str], corpus_glob: str = 'data/*.txt') -> Dict[str, str]:
    """Return {file: excerpt} for docs containing any term."""
    hits = {}
    for txt_path in pathlib.Path('data').glob('*.txt'):
        text = txt_path.read_text(encoding='utf-8', errors='ignore')
        for term in terms:
            m = re.search(fr'.{{0,40}}{re.escape(term)}.{{0,40}}', text, re.I)
            if m:
                hits[txt_path.name] = m.group(0)
                break
    return hits


# ----------------------------------------------------------------------
# 5 · Rank results (simple keyword count)
# ----------------------------------------------------------------------
def rank_results(hits: Dict[str, str], terms: List[str]) -> List[Tuple[str, str]]:
    scored = []
    for f, snippet in hits.items():
        score = sum(snippet.lower().count(t.lower()) for t in terms)
        scored.append((score, f, snippet))
    scored.sort(reverse=True)
    return [(f, s) for score, f, s in scored]


# ----------------------------------------------------------------------
# 6 · Build semantic subgraph (mini graph for CLI display)
# ----------------------------------------------------------------------
def build_semantic_subgraph(entities: Dict[str, str]) -> nx.Graph:
    g = nx.Graph()
    for term, uri in entities.items():
        g.add_node(term, uri=uri, type='entity')
        g.add_node(uri, type='concept')
        g.add_edge(term, uri)
    return g


# ----------------------------------------------------------------------
# 7 · Display
# ----------------------------------------------------------------------
def display_results(ranked: List[Tuple[str, str]], g: nx.Graph):
    print("\n=== Semantic Subgraph (node -- uri) ===")
    for (n1, n2) in g.edges():
        print(f"{n1} -- {n2}")
    print("\n=== Top Results ===")
    for fname, snippet in ranked:
        print(f"\n{fname}:\n  ...{snippet}...")


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python kg_search.py \"<query string>\"")
        sys.exit(1)
    query = sys.argv[1]
    tokens = parse_query(query)
    ents = link_entities_to_kg(tokens)
    expanded = tokens + expand_query_terms(ents)
    hits = retrieve_documents(expanded)
    ranked = rank_results(hits, expanded)
    g = build_semantic_subgraph(ents)
    display_results(ranked, g)

if __name__ == '__main__':
    main()
