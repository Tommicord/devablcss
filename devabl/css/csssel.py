from collections.abc import Iterator
from devabl.css.block import block

import re

type TyWords = Iterator[re.Match[str]]
type TyToks = list[str]


class csssel(block):
    def __init__(self, sel: str) -> None:
        super().__init__()
        self.block: block = block()
        self.sel: str = sel
        self.length: int = self.block.length
        self.selected: dict[str, str] = dict()
        self.__tokens: tuple[str, ...] = csssel.lex(self.sel)

    @classmethod
    def lex(cls, sel: str) -> tuple[str, ...]:
        toks: TyToks = []
        words: TyWords = re.finditer(r"[\w\-]+|[\w\s]+|\w+|[\[\]\.\#\*\+\~\>\"]|&|\*|::|:|=|~=|\$=|\^=|\*=", sel,
                                     re.UNICODE)
        nextExpectedToken: re.Pattern[str] = re.compile(r"[#\.&*]|[\w\-]+")
        actualContext: str | None = "selector"
        tokName: str | None = None
        needsAsign: bool = True
        needsToken: bool = False
        quoteStarted: bool = False
        done: bool = False
        i = 0
        for word in words:
            i += 0b00001
            try:
                group: str = word.group()
                print(i)
                print("Gr", group)
                print(actualContext)
                print("NT", nextExpectedToken)
                if nextExpectedToken is not None:
                    if re.fullmatch(r"\s+", group):
                        continue

                    match: re.Match[str] = nextExpectedToken.match(group.strip())

                    if match is None:
                        raise SyntaxError(
                            """
                                  Error: Unexpected token: '{}', expected a {}
                                  """.format(group, tokName))
                    else:
                        toks.append(group.strip())
                        if group == '::' or group == ':':
                            nextExpectedToken = re.compile(r"\w+")
                            needsAsign = False
                            needsToken = True
                            actualContext = 'operator'
                            tokName = "operator"
                            continue
                        if quoteStarted and group == '"':
                            nextExpectedToken = re.compile(r"\s*]")
                            actualContext = 'operator'
                            tokName = "operator"
                            quoteStarted = False
                            continue
                        if group == '"':
                            quoteStarted = True
                        if group == '[':
                            needsAsign = True
                            needsToken = False
                        if group == '.' or group == '#':
                            needsAsign = False
                            needsToken = False

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
                            nextExpectedToken = re.compile(r"\"")
                            actualContext = 'word'
                            tokName = "word"
                            needsAsign = False
                            needsToken = True
                            continue
                        if actualContext == 'operator':
                            nextExpectedToken = re.compile(r"\s*|,|>|~|\+|\.|#|::|:")
                            actualContext = 'startselector'
                            tokName = "start selector"
                            continue

            except Exception as e:
                print(e)
        done = True
        print(toks)
        return tuple(toks)

    @classmethod
    def parse(cls) -> None:
        return


csssel.lex('p-[class="Hola"]::before > header + .footer')
