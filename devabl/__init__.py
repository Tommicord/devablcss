from devabl.ppipes import conf as _conf
from devabl.ppipes import dist as _dist
from devabl.ppipes import minify as _minify
from devabl.ppipes import watch as _watch
from devabl.pipe import pipe as _pipe
from devabl.pipes import pipes as _pipes
from devabl.cssc import css as _css

__name__ = "devable"
__package__ = "devable"
__version__ = "0.1.0"

css = _css
conf = _conf
minify = _minify
watch = _watch
dist = _dist
pipe = _pipe
pipes = _pipes