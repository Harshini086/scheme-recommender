"""Loads scheme data from data/schemes.json. Swap this module later to load
from a database or government API without touching the recommendation engine."""
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "schemes.json")


def load_schemes():
    """Returns (schemes: list[dict], error: str|None). Never raises."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        schemes = raw.get("schemes", [])
        if not isinstance(schemes, list) or len(schemes) == 0:
            return [], "Scheme dataset is empty."
        return schemes, None
    except FileNotFoundError:
        return [], "Scheme dataset file not found (data/schemes.json)."
    except json.JSONDecodeError:
        return [], "Scheme dataset file is not valid JSON."
    except Exception as e:  # last-resort guard, prototype must never crash
        return [], f"Unexpected error loading schemes: {e}"


def get_categories(schemes):
    return sorted({s.get("category", "Other") for s in schemes})


def get_states(schemes):
    states = set()
    for s in schemes:
        for st in s.get("states", []):
            if st != "All":
                states.add(st)
    return sorted(states)
