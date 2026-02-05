from devabl.cssc import css
from devabl.pipe import pipe
import time
import logging
import os
import os.path as path
import pathlib

logger = logging.getLogger(__name__)

class watch(pipe):
     name: str = "pipes.watch"
     needsContext: bool = True

     def __init__(self, context: css, max_files: int = 1024, seconds: float | int = 0.773444534):
          super().__init__(self.name)
          logging.basicConfig(level=logging.INFO,
                              format='%(asctime)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
          time.sleep(0.4)
          if os.name == "nt":
               os.system('cls')
          else:
               os.system('clear')
          time.sleep(0.4)
          self.files: list[pathlib.Path] = []
          self.running: bool = True
          self._src = context.pipes.get("pipes.conf")["root"]
          self._cached_stamps: list[float] = [x for x in range(max_files)]
          self._path: pathlib.Path = pathlib.Path()

          print("Building...")

          time.sleep(0.9)

          if not path.exists(self._src):
               print("Warning: Source {} does not exist, no such file or directory.".format(self._src))

          while self.running:
               try:
                    time.sleep(seconds)

                    files: list[pathlib.Path] = []
                    for include in context.pipes.get("pipes.conf")["include"]:
                         for file in self._path.glob(include):
                              files.append(file)
                    self.files = files

                    changed = False

                    for i, file in enumerate(self.files):
                         stamp: float = os.stat(file).st_mtime
                         if stamp != self._cached_stamps[i]:
                              changed=True
                              self._cached_stamps[i] = stamp
                              context.pipes.get("pipes.dist").di(context) # Rebuild
                    if changed:
                         logger.info("File Changed : " + str(pathlib.Path(context.pipes.get("pipes.conf")["out"]).absolute()))
               except IndexError: # Max files limit reached
                    print("Fatal Error: Max files limit reached: " + str(max_files))
                    break
               except KeyboardInterrupt:
                    print("Program Terminated!!!")
                    break
               except Exception as e:
                    print("Unknown error! ", e)
          self.running = False