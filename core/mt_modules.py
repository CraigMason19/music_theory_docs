import pkgutil

import music_theory as mt

from core.doc_extractor import DocExtractor


BLACKLISTED_MODULES: list[str] = [
    "mnemonics",
]

def get_available_modules(use_blacklist=True) -> list[str]:
    """
    Returns a list of all available modules in the music_theory package. Can 
    specify if the list returned makes use of the blacklist or not
    """
    modules = [f"{name}" for _, name, is_pkg in pkgutil.iter_modules(mt.__path__)]
    return [m for m in modules if not m in BLACKLISTED_MODULES] if use_blacklist else modules
    


def check_module_for_empty_docstrings(module_name: str) -> None:
    """
    A quick debugging function to look for empty docstrings in modules 
    """
    module = getattr(mt, module_name)
    de = DocExtractor(module)

    print(module_name)

    if(de.module_docstring == None):
        print(f'\tNo module doc')

    for f in de.functions:
        if(f.docstring == None):
            print(f'\t\t{f.name}')

    for c in de.classes:
        if(c.docstring == None):
            print(f'\t\t{c.name}')

        for m in c.methods:
            if(m.docstring == None):
                print(f'\t\t\t{m.name}')


if __name__ == "__main__":
    module_names = get_available_modules(use_blacklist=False)
    
    for name in module_names:      
        check_module_for_empty_docstrings(name)  