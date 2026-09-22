from dataclasses import dataclass

from ajvyra_tts_phoneme_engine import PhonemeEngine


PAD = "<pad>"
UNK = "<unk>"
BOS = "<bos>"
EOS = "<eos>"


@dataclass
class TokenizerState:
    symbol_to_id: dict[str, int]
    id_to_symbol: dict[int, str]


class AJVYRATokenizer:

    def __init__(self):
        self.state = TokenizerState(
            symbol_to_id={},
            id_to_symbol={},
        )

        self.phoneme_engine = PhonemeEngine()

        self._register(PAD)
        self._register(UNK)
        self._register(BOS)
        self._register(EOS)

    def _register(self, symbol: str) -> int:
        if symbol not in self.state.symbol_to_id:
            index = len(self.state.symbol_to_id)

            self.state.symbol_to_id[symbol] = index
            self.state.id_to_symbol[index] = symbol

        return self.state.symbol_to_id[symbol]

    def build_for_language(self, language: str) -> None:
        if language == "fa":
            symbols = [
                "ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح",
                "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش",
                "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق",
                "ک", "گ", "ل", "م", "ن", "و", "ه", "ی",
            ]

        elif language == "ja":
            symbols = [
                "あ", "い", "う", "え", "お",
                "か", "き", "く", "け", "こ",
                "さ", "し", "す", "せ", "そ",
                "た", "ち", "つ", "て", "と",
                "な", "に", "ぬ", "ね", "の",
                "は", "ひ", "ふ", "へ", "ほ",
                "ま", "み", "む", "め", "も",
                "や", "ゆ", "よ",
                "ら", "り", "る", "れ", "ろ",
                "わ", "を", "ん",
            ]

        else:
            raise ValueError(f"Unsupported language: {language}")

        for symbol in symbols:
            self._register(symbol)

        for symbol in [
            "<space>",
            "<.>",
            "<,>",
            "<!>",
            "<? >",
            "<؟>",
            "<。>",
            "<、>",
            "<！>",
            "<？>",
        ]:
            self._register(symbol)

    def encode(self, text: str, language: str) -> list[int]:
        self.build_for_language(language)

        sequence = self.phoneme_engine.encode(
            text,
            language,
        )

        tokens = [self.state.symbol_to_id[BOS]]

        for symbol in sequence.symbols:
            tokens.append(
                self.state.symbol_to_id.get(
                    symbol,
                    self.state.symbol_to_id[UNK],
                )
            )

        tokens.append(self.state.symbol_to_id[EOS])

        return tokens

    def decode(self, tokens: list[int]) -> str:
        symbols = []

        for token in tokens:
            symbol = self.state.id_to_symbol.get(token, UNK)

            if symbol in {PAD, BOS, EOS}:
                continue

            symbols.append(symbol)

        return "".join(
            " " if symbol == "<space>" else symbol
            for symbol in symbols
        )

    @property
    def vocabulary_size(self) -> int:
        return len(self.state.symbol_to_id)
