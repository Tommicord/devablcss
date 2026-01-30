from devabl.css.cssproperty import cssproperty

class block:
    def __init__(self):
        self.block: list[cssproperty] = list()
        self.names: list[str] = list()
        self.ops: bytes = bytearray()
        self.length: int = len(self.block)