from dataclasses import asdict
import sys
from time import time
from pathlib import Path
import json
import logging

import click
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib import request

from src.grammar_example import GrammarExample

"""JLPT Sensei grammar examples downloading tool

This module provides methods to help download grammar rules from 
the https://jlptsensei.com/ website and store them into a json file.
"""


JLPT_SENSEI_URL = "https://jlptsensei.com/"

NX_JLPT_SENSEI_URL_MAP = {
    "N5": JLPT_SENSEI_URL + "jlpt-n5-grammar-list/",
    "N4": JLPT_SENSEI_URL + "jlpt-n4-grammar-list/",
    "N3": JLPT_SENSEI_URL + "jlpt-n3-grammar-list/",
    "N2": JLPT_SENSEI_URL + "jlpt-n2-grammar-list/",
    "N1": JLPT_SENSEI_URL + "jlpt-n1-grammar-list/",
}


def fetch_grammar_rule(url: str) -> list[GrammarExample]:
    """Fetch examples for a grammar rule

    Fetch all grammar examples for a single grammar rule
    from the provided url.

    Returns
    -------
    examples: list[GrammarExample]
        List of grammar examples fetched. 
    """
    html_data = request.urlopen(url).read()
    bs = BeautifulSoup(html_data, features="html.parser")

    try:
        rule_examples = bs.find(
            "div", {"id": "examples"}
        ).select('div[class*="example-cont"]')
    except:
        logging.warn(f"Could not fetch grammar examples from url `{url}`")
        return []

    res = []
    meaning = bs.find(
        "div", {"id": "meaning"},
    ).find(
        "p", {"class": "eng-definition"}
    ).text

    jlpt_level = bs.find(
        "p", {"class": "glm-level"},
    ).find("a").text

    for rule_example in rule_examples:
        name = rule_example["id"]
        hiragana_transliteration = rule_example.find(
            "div", {"id": name + "_ja"},
        ).text
        english_translation = rule_example.find(
            "div", {"id": name + "_en"},
        ).text
        japanese_sentence = rule_example.select(
            'div[class*="example-main"]'
        )[0].text
        colored_japanese_sentence = "".join([str(c) for c in rule_example.select(
            'div[class*="example-main"]'
        )[0].find("p").contents])
        res.append(
            GrammarExample(
                jlpt_level=jlpt_level,
                meaning=meaning,
                english_translation=english_translation,
                japanese_sentence=japanese_sentence,
                colored_japanese_sentence=colored_japanese_sentence,
                hiragana_transliteration=hiragana_transliteration,
            )
        )

    return res


def fetch_nx_page(url: str) -> list[GrammarExample]:
    """Fetch grammar examples for a specific page

    Fetch all grammar examples from a single page pages for a
    specific Nx level from the provided url.

    Returns
    -------
    examples: list[GrammarExample]
        List of grammar examples fetched. 
    """
    html_data = request.urlopen(url).read()
    bs = BeautifulSoup(html_data, features="html.parser")

    grammar_rules = bs.find(
        "table", {"id": "jl-grammar"}
    ).find("tbody").find_all(
        "tr", {"class": "jl-row"}
    )

    res = []

    for grammar_rule in tqdm(
        grammar_rules, 
        desc="Fetching grammar rules",
        file=sys.stdout,
        position=2,
        leave=False,
    ):
        res += fetch_grammar_rule(
            grammar_rule.find("a", {"class": "jl-link"})["href"]
        )
        


    return res

def fetch_nx_pages(url: str) -> list[GrammarExample]:
    """Fetch grammar examples for a specific Nx level

    Fetch all grammar examples from all pages for a specific Nx level from the
    provided url.

    Returns
    -------
    examples: list[GrammarExample]
        List of grammar examples fetched. 
    """
    html_data = request.urlopen(url).read()
    bs = BeautifulSoup(html_data, features="html.parser")

    res = []

    page_items = bs.find(
        "ul", {"class": "pagination"}
    ).find_all(
        "a", {"class": "page-numbers"}
    )

    for page_item in tqdm(
        page_items, 
        desc="Fetching Nx pages",
        file=sys.stdout,
        position=1,
        leave=False,
    ):
        res += fetch_nx_page(
            url=page_item["href"],
        )

    return res


def fetch_all() -> list[GrammarExample]:
    """Fetch all grammar examples

    Fetch all grammar examples available on the JLPT-Sensei website using
    urllib and beautifulsoup.

    Returns
    -------
    examples: list[GrammarExample]
        List of grammar examples fetched. 
    """
    time_start = time()
    logging.info(f"Fetching all grammar examples from `{JLPT_SENSEI_URL}`")

    examples = []
    for _,url in tqdm(
        NX_JLPT_SENSEI_URL_MAP.items(), 
        desc="Fetching Nx levels",
        file=sys.stdout,
        position=0,
        leave=False,
    ):
        examples += fetch_nx_pages(url=url)

    time_end = time()
    logging.info(f"Fetched {len(examples)} grammar examples from `{JLPT_SENSEI_URL}` in {time_end - time_start:0.5} seconds")

    return examples


def examples_to_json(
    examples: list[GrammarExample],
    output_file: Path,
) -> None:
    """Save examples to JSON file

    Save a list of examples into a JSON file

    Parameters
    ----------
    examples: list[GrammarExample]
        The list of grammar examples to store into the json file
    output_file: Path
        The output JSON file to save outputs to
    """
    logging.info(f"Saving to file `{output_file}`")
    with open(output_file, "w") as f:
        f.write(
            json.dumps(
                [
                    asdict(i) for i in examples
                ],
                ensure_ascii=False,
                indent=4,
            )
        )
    logging.info(f"Saved to file `{output_file}`")


@click.command()
@click.argument('output_file', prompt="Output file to store grammar examples", type=click.Path(False))
def create_grammar_file(
    output_file: Path,
) -> None:
    """Create grammar file
    
    Click entry point.

    Parameters
    ----------
    output_file: Path
    """
    examples_to_json(
        examples=fetch_all(),
        output_file=output_file,
    )
    

if __name__ == "__main__":
    create_grammar_file()