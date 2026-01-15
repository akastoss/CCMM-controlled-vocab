import os
import sys
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS

# Usage: python convert_csv_to_ttl.py AgentRole
vocab_name = sys.argv[1] if len(sys.argv) > 1 else None
if not vocab_name:
    raise ValueError("Chybí parametr: název slovníku (např. AgentRole).")

csv_file = f"{vocab_name}.csv"
ttl_file = f"{vocab_name}.ttl"

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Soubor {csv_file} nebyl nalezen ve složce.")

df = pd.read_csv(csv_file)

g = Graph()
g.bind("rdf", RDF)
g.bind("skos", SKOS)

AGENT = Namespace(f"https://vocabs.ccmm.cz/registry/codelist/{vocab_name}/")
g.bind("", AGENT)

for _, row in df.iterrows():
    concept_uri = URIRef(row["IRI"])
    g.add((concept_uri, RDF.type, SKOS.Concept))
    g.add((concept_uri, SKOS.prefLabel, Literal(row["title_en"], lang="en")))
    g.add((concept_uri, SKOS.prefLabel, Literal(row["title_cs"], lang="cs")))

    if pd.notna(row["definition_en"]):
        g.add((concept_uri, SKOS.definition, Literal(row["definition_en"], lang="en")))
    if pd.notna(row["definition_cs"]):
        g.add((concept_uri, SKOS.definition, Literal(row["definition_cs"], lang="cs")))

    if pd.notna(row["parentId"]):
        parent_row = df[df["id"] == row["parentId"]]
        if not parent_row.empty:
            parent_uri = URIRef(parent_row.iloc[0]["IRI"])
            g.add((concept_uri, SKOS.broader, parent_uri))

g.serialize(destination=ttl_file, format="turtle")

print(f"Soubor {ttl_file} byl úspěšně vytvořen.")
