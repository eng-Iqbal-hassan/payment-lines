PREFIXES = ("POS ", "ATM WDL ", "IBFT IN ")


def normalize(text:str) -> str:
    text = text.upper().strip()
    for p in PREFIXES:
        if text.startswith(p):
            text = text[len(p):]
    text = text.replace(".PK", "")
    return text.split()[0]