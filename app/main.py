from typing import List
from collections import defaultdict
import json


PRICAT_FILE = "pricat.csv"
MAPPINGS_FILE = "mappings.csv"
CATALOGUE_FILE = "catalogue.json"
ARTICLE_NUMBER = "article_number"
SOURCE, DESTINATION, SOURCE_TYPE, DESTINATION_TYPE = "source", "destination", "source_type", "destination_type"
ARTICLES, VARIATIONS = "articles", "variations"


def main():
    """Load pricat and mapping files and generate a structured JSON file for the catalogue"""
    print("Loading input files")
    with open(PRICAT_FILE, "r") as f:
        variations = interpret_pricat(file=f.read())

    with open(MAPPINGS_FILE, "r") as f:
        mapping = interpret_mapping(file=f.read())

    print("Mapping variations and creating structured catalogue")
    mapped_variations = apply_mapping(mapping=mapping, unmapped_variations=variations)
    articles = group_articles(mapped_variations)
    articles = move_variant_attributes_up(articles=articles)
    catalogue = move_article_attributes_up(articles=articles)

    with open(CATALOGUE_FILE, "w") as f:
        json.dump(catalogue, f, indent=2)
        print("The json file is created")


def interpret_pricat(file: str) -> (List[dict], List[str]):
    """Interpret the pricat file line by line"""
    variations, keys = [], []
    for i, line in enumerate(file.split("\n")):
        if i == 0:
            # Interpret header
            keys = line.split(";")
        else:
            variations.append({keys[j]: v for j, v in enumerate(line.split(";"))})

    return variations


def interpret_mapping(file: str):
    """Interpret the mapping file line by line"""
    mapping = []
    for i, line in enumerate(file.split("\n")):
        if i == 0:
            continue
        split_line = line.split(";")
        mapping.append(
            {
                SOURCE: split_line[0].split("|"),
                DESTINATION: split_line[1],
                SOURCE_TYPE: split_line[2].split("|"),
                DESTINATION_TYPE: split_line[3],
            }
        )
    return mapping


def apply_mapping(mapping: List[dict], unmapped_variations: List[dict]) -> List[dict]:
    """Apply the mapping to the variants.
    Any empty fields will be deleted on a variation-by-variation basis.
    If the type of a mapping field is recognised but the value is not,
    the old field is persisted and no new field is created."""
    mapped_variations = []
    for variation in unmapped_variations:
        # Start with all not-empty values
        mapped_var = {k: v for k, v in variation.items() if v}

        # Map values. It no matching mapping is found, the original values are persisted
        for m in mapping:
            source = [variation[t] for t in m[SOURCE_TYPE]]
            if m[SOURCE] == source:
                # First remove the old value(s)
                for t in m[SOURCE_TYPE]:
                    mapped_var.pop(t)
                # Then add the new mapped value
                mapped_var[m[DESTINATION_TYPE]] = m[DESTINATION]

        mapped_variations.append(mapped_var)
    return mapped_variations


def group_articles(mapped_variations: List[dict]) -> List[dict]:
    """Variants are grouped based on the article number field"""
    articles_dict = defaultdict(list)
    for variation in mapped_variations:
        article_number = variation[ARTICLE_NUMBER]
        articles_dict[article_number].append(variation)
        variation.pop(ARTICLE_NUMBER)

    articles = [{ARTICLE_NUMBER: k, VARIATIONS: v} for k, v in articles_dict.items()]
    return articles


def move_variant_attributes_up(articles: List[dict]) -> List[dict]:
    """Any variant fields that are the same for all variants in the article are moved up to the article level"""
    for a in articles:
        keys = [k for k in a[VARIATIONS][0].keys()]
        for k in keys:
            values = [v[k] for v in a[VARIATIONS]]
            if len(set(values)) == 1:
                # Add value to article and remove from variations in article
                a[k] = values[0]
                for v in a[VARIATIONS]:
                    v.pop(k)

    return articles


def move_article_attributes_up(articles: List[dict]) -> dict:
    """Any article fields that are the same for all articles in the catalogue are moved up to the catalogue level"""
    catalogue = {ARTICLES: articles}
    keys = [k for k in articles[0].keys() if k != VARIATIONS]
    for k in keys:
        values = [v[k] for v in articles]
        if len(set(values)) == 1:
            # Add value to article and remove from variations in article
            catalogue[k] = values[0]
            for v in articles:
                v.pop(k)

    return catalogue


if __name__ == "__main__":
    main()
