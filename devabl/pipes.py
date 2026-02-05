from devabl.pipe import pipe

class pipes:
     def __init__(self, context) -> None:
         self.res: dict[str | int, any] = {}
         self.context = context

     def pipe(self, fn: 'pipe', *args: tuple[any], **kwargs: dict[str, any]) -> 'pipes':
          try:
               if isinstance(fn, pipe) or fn.__bases__[0] == pipe:
                    if fn.needsContext:
                         self.res[fn.name] = fn(self.context, *args, **kwargs)
                    else:
                         self.res[fn.name] = fn(*args, **kwargs)
               return self
          except Exception as e:
               print("Fatal Error in pipe function '{}': {}".format(fn.name, str(e)))
               return self

     def get(self, k: str | int) -> any:
          try:
               return self.res[k]
          except KeyError:
               print(f"Fatal Error: Key '{k}' not found in pipelist")
               return None