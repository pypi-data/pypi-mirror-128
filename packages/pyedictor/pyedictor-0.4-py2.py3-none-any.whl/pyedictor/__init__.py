__version__ = '0.4'
from pyedictor.util import fetch
import lingpy

def cldf2wl(path, namespace=None, addon=None,
        preprocessing=None):
    
    namespace=namespace or dict([
                ("language_id", "doculect"),
                ("concept_name", "concept"),
                ("value", "value"),
                ("form", "form"),
                ("segments", "tokens"),
                ("comment", "note")
                ])
    addon = addon or {}
    namespace.update(addon)
    columns = list(namespace)
    
    return lingpy.basic.wordlist.Wordlist.from_cldf(
            path,
            columns=columns,
            namespace=namespace)

