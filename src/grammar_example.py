from dataclasses import dataclass

@dataclass
class GrammarExample:
    jlpt_level: str
    meaning: str
    japanese_sentence: str
    colored_japanese_sentence: str
    english_translation: str
    hiragana_transliteration: str