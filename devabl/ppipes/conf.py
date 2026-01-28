from devabl.pipe import pipe

class conf(pipe):
     name: str = "pipes.conf"
     needsContext: bool = False

     def __init__(self, options: dict[str, str]) -> None:
          super().__init__(self.name)
          self.options = dict()
          for k,v in options.items():
               self.options[k] = v

     def __getitem__(self, key: str) -> str:
          try:
               return self.options[key]
          except KeyError:
               raise KeyError(f"Fatal Error: Key '{key}' not found in conf options.")