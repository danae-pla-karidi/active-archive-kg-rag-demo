# active-archive-kg-rag-demo
Preliminary open-source demo of the Active-Archive pipeline—showcasing KG-guided search and RAG-assisted curation—built on a subset of ESG sustainability reports drawn from https://huggingface.co/datasets/DataNeed/company-reports


# Run the RAG curation pipeline on the sample PDF
python -m active_archives.rag_curation data/sample_report.pdf

# Try a knowledge-graph-guided search query
python -m active_archives.kg_exploration "Company A CO2 2025"
