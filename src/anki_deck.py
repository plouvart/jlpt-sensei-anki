import genanki
import json
from pathlib import Path
from dataclasses import asdict
import random

import click

from src.grammar_example import GrammarExample


CARD_CSS = """
.color {
	color: red;
	font-weight: bold;
}
        
.level {
	background-color: white;
	border: 1px solid green;
}

.template {
	text-decoration: underline;
}

.hiragana {
	 font-size: 12px;
}
"""

CARD_FRONT = """
<span class="level">{{jlpt_level}} </span>
&nbsp; &nbsp; &nbsp; &nbsp;
<span class="template">{{meaning}}</span>
<br><br>
{{english_translation}}
<br><br>
{{type:japanese_sentence}}
"""

CARD_BACK = """
{{FrontSide}}<hr id="answer">
<br>
{{colored_japanese_sentence}}
<br><br>
<span class="hiragana">{{hiragana_transliteration}}</span>
"""

@click.command()
@click.argument('input_file', prompt="Input json file coontaining grammar examples", type=click.Path(False))
@click.argument('output_file', prompt="Output anki deck file", type=click.Path(False))
def create_grammar_deck(
    input_file: Path,
    output_file: Path,
) -> None:
    """Create an Anki deck from grammar examples
    
    Create an Anki deck using grammar examples from the provided
    JSON file.

    Parameters
    ----------
    input_file: Path
        The input JSON file containing the grammar examples to use
    output_file: Path
        The output Anki deck file to create. Should have an `.apkg` extension.
    """
    model_id = random.randint(0, 1<<32)
    grammar_model = genanki.Model(
        model_id=model_id,
        name='Interactive Japanese Grammar Model',
        fields=list(
            GrammarExample.__dataclass_fields__.keys()
        ),
        templates=[
            {
            'name': 'Card 1',
            'qfmt': CARD_FRONT,
            'afmt': CARD_BACK,
            },
        ],
        css=CARD_CSS,
    )

    deck_id = random.randint(0, 1<<32)
    grammar_deck = genanki.Deck(
        deck_id=deck_id,
        name='Interactive Japanese Grammar Deck',
        description='A Japanese Grammar Deck that requires you to translate english sentences into Japanese',
    )

    with open(input_file, "r") as f:
        for grammar_example in json.loads(f.read()):
            grammar_deck.add_note(
                genanki.Note(
                    model=grammar_model,
                    fields=list(
                        asdict(
                            GrammarExample(**grammar_example)
                        ).values()
                    )
                )
            )

    genanki.Package(grammar_deck).write_to_file(output_file)

if __name__ == "__main__":
    create_grammar_deck()