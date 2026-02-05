from collections.abc import Iterator
from devabl.css.block import block
from colorama import init as colorinit
from colorama import Fore

import re

type TyWords = Iterator[re.Match[str]]
type TyMutableToks = list[str]
type TyToks = tuple[str, ...]
type TySynt = tuple

colorinit(autoreset=True)

class csssel(block):
    def __init__(self, sel: str) -> None:
        super().__init__()
        self.block: block = block()
        self.sel: str = sel
        self.length: int = self.block.length
        self.__tokens: TyToks = csssel.lex(self.sel)
        self.__synt: TySynt = csssel.synt(self.__tokens)

    @classmethod
    def lex(cls, sel: str) -> tuple[str, ...]:
        toks: TyMutableToks = []
        words: TyWords = re.finditer(r"[\w\-]+|[\w\s]+|\w+|[\[\]\.\#\*\+\~\>\"\']|&|\*|::|:|=|~=|\$=|\^=|\*=", sel,
                                     re.UNICODE)
        for word in words:
            group = word.group().strip()

            if re.fullmatch(r"\s+", group) or not group:
                continue

            toks.append(group)

        return tuple(toks)

    @classmethod
    def synt(cls, toks: tuple[str,...]):
        nextExpectedToken: re.Pattern[str]
        actualContext: str | None
        tokName: str | None
        if not re.match(r"[.#&]",toks[0], re.UNICODE):
            nextExpectedToken = re.compile(r"[\w\-]+", re.UNICODE)
            actualContext = "selector"
            tokName = "selector"
        else:
            nextExpectedToken = re.compile(r"\[|::|:|\s*|,|>|~|\+|\.|#")
            actualContext = "word"
            tokName = "word"
        needsAsign: bool = False
        needsToken: bool = False
        needsAttribSelector: bool = True
        quoteStarted: bool = False
        for tok in toks:
            if re.fullmatch(r"\s+", tok) or not tok:
                continue

            if tok == ']' and actualContext == 'attrtoken':
                nextExpectedToken = re.compile(r"\s*]")
                actualContext = 'operator'
                tokName = 'operator'

            match: re.Match[str] | None = nextExpectedToken.match(tok)

            if match is None:
                print("{}Error: Unexpected token: '{}', expected a {}".format(Fore.RED, tok, tokName))
                break
            else:
                if tok == '::' or tok == ':':
                    nextExpectedToken = re.compile(r"\w+")
                    needsAsign = False
                    needsToken = True
                    actualContext = 'operator'
                    tokName = "operator"
                    continue
                if quoteStarted and tok == '"':
                    nextExpectedToken = re.compile(r"\s*]")
                    actualContext = 'operator'
                    tokName = "operator"
                    quoteStarted = False
                    needsAttribSelector = False
                    needsToken = False
                    needsAsign = False
                    continue
                if tok == '"':
                    quoteStarted = True

                if actualContext == 'startselector':
                    nextExpectedToken = re.compile(r"[.#&]?")
                    actualContext = 'word'
                    tokName = "word"
                    needsAsign = False
                    needsToken = False
                    needsAttribSelector = True
                    continue

                if tok == '[':
                    needsAsign = True
                    needsToken = False
                    needsAttribSelector = False

                if actualContext == 'selector':
                    nextExpectedToken = re.compile(r"\[|::|:|\s*|,|>|~|\+|\.|#")
                    actualContext = 'word'
                    tokName = "word"
                    continue

                if actualContext == 'word':
                    nextExpectedToken = re.compile(r"[\w\-]+")
                    if needsAsign:
                        actualContext = 'attrassign'
                        tokName = "assign operator"
                        continue
                    elif needsToken:
                        actualContext = 'attrtoken'
                        tokName = "token"
                        continue
                    elif needsAttribSelector:
                        actualContext = 'selector'
                        tokName = "selector"
                        continue
                    else:
                        actualContext = 'operator'
                        tokName = "operator"
                        continue
                if actualContext == 'attrassign':
                    nextExpectedToken = re.compile(r"=|~=|\$=|\^=|\*=")
                    actualContext = 'attrtoken'
                    tokName = "token"
                    continue
                if actualContext == 'attrtoken':
                    nextExpectedToken = re.compile(r"\"?")
                    actualContext = 'word'
                    tokName = "word"
                    needsAsign = False
                    needsToken = True
                    needsAttribSelector = False
                    continue
                if actualContext == 'operator':
                    nextExpectedToken = re.compile(r"(\s*|,|>|~|\+|\.|#|::|:)?")
                    actualContext = "startselector"
                    tokName = "start selector"
                    continue

        return tuple() # TODO: Fix this


csssel('hola-fi[class="Hola"]::before .hola')