# Convert_AgentRole.py
# Autor: Pavel Kotlík
# Převod slovníku AgentRole.csv do RDF/Turtle (SKOS)
# Python 3.13.5, vyžaduje knihovny: pandas, rdflib

import os
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS

if not os.path.exists("AgentRole.csv"):
    raise FileNotFoundError("Soubor AgentRole.csv nebyl nalezen ve složce.")

df = pd.read_csv("AgentRole.csv")

g = Graph()
g.bind("rdf", RDF)
g.bind("skos", SKOS)

AGENT = Namespace("https://vocabs.ccmm.cz/registry/codelist/AgentRole/")
g.bind("", AGENT)

for _, row in df.iterrows():
    concept_uri = URIRef(row['IRI'])
    g.add((concept_uri, RDF.type, SKOS.Concept))
    g.add((concept_uri, SKOS.prefLabel, Literal(row['title_en'], lang='en')))
    g.add((concept_uri, SKOS.prefLabel, Literal(row['title_cs'], lang='cs')))

    if pd.notna(row['definition_en']):
        g.add((concept_uri, SKOS.definition, Literal(row['definition_en'], lang='en')))
    if pd.notna(row['definition_cs']):
        g.add((concept_uri, SKOS.definition, Literal(row['definition_cs'], lang='cs')))

    if pd.notna(row['parentId']):
        parent_row = df[df['id'] == row['parentId']]
        if not parent_row.empty:
            parent_uri = URIRef(parent_row.iloc[0]['IRI'])
            g.add((concept_uri, SKOS.broader, parent_uri))

g.serialize(destination="AgentRole.ttl", format="turtle")

print("Soubor AgentRole.ttl byl úspěšně vytvořen.")
