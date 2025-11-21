import unicodedata
import re

# ---------------------------------------------------------
# STRING NORMALIZÁLÁS
# ---------------------------------------------------------

def normalize_text(text: str):
    """
    Név normalizálás:
    - ékezet eltávolítás
    - kisbetűsítés
    - speciális karakterek törlése
    """

    if not isinstance(text, str):
        return ""

    # ékezet eltávolítás
    nfkd = unicodedata.normalize('NFKD', text)
    no_accents = "".join([c for c in nfkd if not unicodedata.combining(c)])

    # kisbetű
    lowered = no_accents.lower()

    # nem betű-szám eltávolítása
    clean = re.sub(r'[^a-z0-9 ]', '', lowered)

    # dupla whitespace tisztítás
    clean = " ".join(clean.split())

    return clean.strip()


# ---------------------------------------------------------
# ALIAS ADATBÁZIS (a legfontosabbak)
# ---------------------------------------------------------

TEAM_ALIASES = {
    "man united": "manchester united",
    "man utd": "manchester united",
    "man city": "manchester city",
    "psg": "paris saint germain",
    "real": "real madrid",
    "bayern": "bayern munich",
    "lakers": "los angeles lakers",
    "bucks": "milwaukee bucks",
    "leafs": "toronto maple leafs",
    "bolts": "tampa bay lightning",
    "tb lightning": "tampa bay lightning"
}


def alias(text: str):
    """
    Ha a csapatnév szerepel az alias listában,
    visszaadjuk a standardizált formát.
    """
    norm = normalize_text(text)
    if norm in TEAM_ALIASES:
        return TEAM_ALIASES[norm]
    return norm


# ---------------------------------------------------------
# NÉV EGYEZTETÉS
# ---------------------------------------------------------

def match_team_name(name1: str, name2: str):
    """
    Két név hasonlóságának ellenőrzése:
    - normalizált string összehasonlítás
    - alias konverzió
    """

    n1 = alias(name1)
    n2 = alias(name2)

    return n1 == n2
