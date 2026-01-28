class pipe:
     needsContext: bool = False
     
     def __init__(self, name: str) -> None:
          self.name: str = name

     def __init_subclass__(cls):
          pass

     def __repr__(self) -> str:
          return f"pipe(name='{self.name}')"