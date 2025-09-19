import music_theory as mt

def parse_bool(value: str | None) -> bool:
    return str(value).strip().lower() == "true"

def parse_note(value: str | int) -> mt.Note:
    try:
        index = int(value)
        return mt.Note.from_index(index)
    
    except (ValueError, IndexError):
        raise ValueError(f"Invalid note index: {value}")

def parse_key_type(value: str | int) -> mt.KeyType:
    try:
        index = int(value)
        return mt.KeyType.items()[index]
    
    except (ValueError, IndexError):
        raise ValueError(f"Invalid key type index: {value}")