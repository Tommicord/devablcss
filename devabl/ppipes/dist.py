from devabl.pipe import pipe
from devabl.css import css

class dist(pipe):
     name: str = "pipes.dist"
     needsContext: bool = True

     def __init__(self, context: css, open: bool) -> None:
          super().__init__(self.name)
     
          if open:
               dist.di(context=context)
               
     @classmethod
     def di(cls, context: css):               
          try:
               with open(context.pipes.get("pipes.conf")["out"], "w", encoding="utf-8") as f:
                    f.write(context.code)
          except IOError as e:
               raise SystemError(f"Error: Unable to write to the file {e}")