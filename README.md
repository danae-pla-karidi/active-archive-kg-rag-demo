# active-archive-kg-rag-demo
Preliminary open-source demo of the Active-Archive pipeline—showcasing KG-guided search and RAG-assisted curation—built on a subset of ESG sustainability reports drawn from https://huggingface.co/datasets/DataNeed/company-reports


# RAG-based curation (auto-approves suggestion)
python src/rag_curation.py data/sample_report.pdf

# KG-guided search
python src/kg_search.py "Company A 2025 CO2"****
