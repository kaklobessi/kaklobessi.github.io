"""
Fetch citation data from Google Scholar and save to docs/citations_gs.json
Run: python fetch_scholar.py
"""
import json
from scholarly import scholarly

AUTHOR_ID = "LH6CiwUAAAAJ"

print("Fetching Google Scholar profile...")
author = scholarly.search_author_id(AUTHOR_ID)
author = scholarly.fill(author, sections=["publications", "indices", "counts"])

# Global stats
output = {
    "total_citations": author.get("citedby", 0),
    "h_index": author.get("hindex", 0),
    "i10_index": author.get("i10index", 0),
    "citedby_year": author.get("cites_per_year", {}),
    "papers": []
}

# Per-paper stats
for pub in author.get("publications", []):
    try:
        filled = scholarly.fill(pub)
        bib = filled.get("bib", {})
        output["papers"].append({
            "title": bib.get("title", ""),
            "year": bib.get("pub_year", ""),
            "cited_by_count": filled.get("num_citations", 0),
            "journal": bib.get("journal", ""),
        })
        print(f"  ✓ {bib.get('title','')[:60]} — {filled.get('num_citations',0)} citations")
    except Exception as e:
        print(f"  ✗ Error on paper: {e}")

# Save
out_path = "docs/citations_gs.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to {out_path}")
print(f"Total citations: {output['total_citations']} | h-index: {output['h_index']} | i10: {output['i10_index']}")
