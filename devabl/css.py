from devabl.pipes import pipes

class css:
     def __init__(self) -> None:
          self.code: str = ""
          self.pipes: pipes = pipes(self)

     def pipelist(self, res: pipes) -> None:
          return True
          
     def debug(self) -> None:
          self.pipes.debug()