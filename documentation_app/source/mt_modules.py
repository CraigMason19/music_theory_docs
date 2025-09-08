import pkgutil

import music_theory as mt

BLACKLISTED_MODULES: list[str] = [
    "mnemonics",
]

def get_available_modules() -> list[str]:
    return [
        f"{name}"
        for _, name, is_pkg in pkgutil.iter_modules(mt.__path__)
        if not name in BLACKLISTED_MODULES
    ]