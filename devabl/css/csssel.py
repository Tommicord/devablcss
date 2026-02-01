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
          words: TyWords = re.finditer(r"\w+|\w+?=\[|[\[\]\.\#\*\+\~\>\"]|&|\*|::|:|=|~=|\$=|\^=|\*=]", sel, re.UNICODE)
          toks: TyToks = []
          tokName: str = "start selector"
          nextExpectedToken: re.Pattern[str] | None = re.compile(r"[#\.&*]")
          actualContext: str | None = "startselector"
          needsAsign: bool = True
          quoteStarted: bool = False
          bracketStarted: bool = False
          done: bool = False
          i = 0
          for word in words:
              i += 0b00001
              try:
                   group: str | bytes = word.group()
                   print(i)
                   print("Gr", group)
                   print(actualContext)
                   print("NT", nextExpectedToken)
                   if nextExpectedToken is not None:
                        match: re.Match[str] = nextExpectedToken.match(group)

                        if match is None:
                             raise SyntaxError(
                                  """
                                  Error: Unexpected token: '{}', expected a {}
                                  """.format(group, tokName))
                        else:
                             if actualContext == 'startselector':
                                    nextExpectedToken = re.compile(r"\w+", re.UNICODE)
                                    actualContext = "selector"
                                    tokName = "selector"
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
                                   bracketStarted = True
                             if group == ']':
                                   bracketStarted = False
                             if actualContext == 'selector':
                                  nextExpectedToken = re.compile(r"\[|::|:|\s*|,|>|~|\+|\.|#")
                                  needsAsign = True
                                  actualContext = 'word'
                                  tokName = "word"
                                  continue
                             if actualContext == 'word':
                                   nextExpectedToken = re.compile(r"\w+")
                                   if needsAsign:
                                        actualContext = 'attrassign'
                                        tokName = "assign operator"
                                   else:
                                        actualContext = 'attrtoken'
                                        tokName = "token"
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
                                 continue
                             if actualContext == 'operator':
                                 nextExpectedToken = re.compile(r"\s*|,|>|~|\+|\.|#|\w+|::|:")
                                 actualContext = 'startselector'
                                 tokName = "start selector"
                                 continue

              except Exception as e:
                  print(e)
          # TODO: Fix this
          done = True
          print(toks)
          return tuple(toks)

     @classmethod
     def parse(cls) -> None:
         return



csssel.lex(".hola[class$=\"MyPrueba es\"] > .mundo + .algo")
