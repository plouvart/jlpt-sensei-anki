# jlpt-sensei-anki

This is a small repository containing methods to **retrieve all/most of the grammar examples from [JLPT-sensei](https://jlptsensei.com/)** into a JSON formatted file.

This repository also contains code to transform this **JSON file into an Anki deck**!

I wrote this because JLPT-sensei has some really good examples, but none of those are on Anki.
Acutally.. some guy built a few Anki decks using the JLPT-sensei flash cards, but those are just images.
To better learn Japanese grammar, I think it is better to have the user translate an english sentence into japanese using his keyboard, rather than just
showing him a flashcard.
You can't do this with JLPT-sensei flashcard alone, you need the text itself. Not to mention a lot of the sentence examples are not included anyway.

So here it is, this repo gives you access a very useful deck for learning Japanese grammar!
I may even upload it on Ankiweb if I have time.
Here's a few screenshots of how it looks in action (using Anki for android).

Question                   |  Answer
:-------------------------:|:-------------------------:
![Front of the Anki card](https://github.com/plouvart/jlpt-sensei-anki/blob/master/res/question.png) | ![Back of the Anki card](https://github.com/plouvart/jlpt-sensei-anki/blob/master/res/answer.png)

## Installation

This project uses poetry.
Use the following command at the root of the project to install it
```bash
poetry install
```

## Usage

This project uses click to easily interact via the command line.

After installing the project with poetry, you should be able to
to download the grammar examples with the following command:
```bash
poetry run python3  src/jlpt_sensei_download.py  json_file_you_want.json
```

And to create the associated Anki deck:
```bash
poetry run python3 src/anki_deck.py   json_file_you_want.json   deck_file.apkg
```

## Credit

- [JLPT-sensei website](https://jlptsensei.com/) for those great and extensive grammar examples.
- Anki and genanki devs.



