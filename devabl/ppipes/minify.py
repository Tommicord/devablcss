from devabl.pipe import pipe
from devabl.cssc import css

import re

class minify(pipe):
     name: str = "pipes.minify"
     needsContext: bool = True

     def __init__(self, context: css) -> None:
          super().__init__(self.name)
          css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", context.code )
          css = re.sub( r'/\*[\s\S]*?\*/', "", css )
          css = css.replace( "$$HACK1$$", '/**/' )
          css = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', css )
          css = re.sub( r'\s+', ' ', css )
          css = re.sub( r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css )
          css = re.sub( r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css )

          for rule in re.findall( r'([^{]+){([^}]*)}', css ):
               properties = {}
               porder = []
               for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
                    key = prop[0].strip().lower()
                    if key not in porder: porder.append( key )
                    properties[ key ] = prop[1].strip()
          context.code = css

          print(context.code)