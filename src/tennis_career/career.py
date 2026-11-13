"""Read and clean career match results from Tennis Abstract."""
import json
import re
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

BASE = "https://www.tennisabstract.com"


def _player_slug(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Please enter a player's first and last name.")
    parts = re.findall(r"[A-Za-z]+", name.strip())
    slug = "".join(part[0].upper() + part[1:] for part in parts)
    if not slug or len(slug) < 3:
        raise ValueError("Please enter a valid player name.")
    return slug[0].upper() + slug[1:]


def _read_url(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (student project)"})
    try:
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ValueError("Could not find the player or retrieve their data from Tennis Abstract.") from exc


def _extract_matches(js):
    match = re.search(r"\bvar\s+morematchmx\s*=\s*(\[)", js)
    if not match:
        raise ValueError("No career match table was found in the JavaScript file.")
    try:
        matches, _ = json.JSONDecoder().raw_decode(js[match.start(1):])
    except json.JSONDecodeError as exc:
        raise ValueError("The career match table could not be read.") from exc
    if not isinstance(matches, list) or not matches:
        raise ValueError("No matches were found for this player.")
    return matches


def _get_birthday(page):
    match = re.search(r"Age:\s*\d+\s*\((\d{2}-[A-Za-z]{3}-\d{4})\)", page)
    if not match:
        match = re.search(r"\((\d{2}-[A-Za-z]{3}-\d{4})\)", page)
    if not match:
        raise ValueError("Could not determine this player's date of birth.")
    return datetime.strptime(match.group(1), "%d-%b-%Y")


def _opponent_age(row, played):
    field = str(row[16]).strip() if len(row) > 16 else ""
    if re.fullmatch(r"\d{8}", field):
        try:
            birthday = datetime.strptime(field, "%Y%m%d")
            return (played - birthday).days / 365.2425
        except ValueError:
            return None
    try:
        return float(field)
    except ValueError:
        return None


def _clean_match(row, birthday):
    if not isinstance(row, list) or len(row) < 17 or row[4] not in ("W", "L"):
        return None
    try:
        played = datetime.strptime(str(row[0]), "%Y%m%d")
    except ValueError:
        return None
    age = (played - birthday).days / 365.2425
    opponent_age = _opponent_age(row, played)
    if opponent_age is None or not 12 <= opponent_age <= 60 or not 12 <= age <= 60:
        return None
    return (played.date().isoformat(), row[11], age, opponent_age,
            age - opponent_age, "Win" if row[4] == "W" else "Loss")


def clean_career_js(js, birthday):
    """Convert career JavaScript and a player's birthday to a plot-ready DataFrame."""
    if isinstance(birthday, str):
        birthday = datetime.strptime(birthday, "%Y-%m-%d")
    rows = [_clean_match(row, birthday) for row in _extract_matches(js)]
    columns = ["match_date", "opponent", "player_age", "opponent_age", "age_difference", "result"]
    data = pd.DataFrame([row for row in rows if row is not None], columns=columns)
    if data.empty:
        raise ValueError("No matches with valid ages and results were found.")
    return data.sort_values("match_date").reset_index(drop=True)


def get_career_matches(name):
    """Download and clean career matches for a tennis player by name."""
    slug = _player_slug(name)
    js = _read_url(f"{BASE}/jsmatches/{slug}Career.js")
    for prefix in ("player", "wplayer"):
        try:
            page = _read_url(f"{BASE}/cgi-bin/{prefix}-classic.cgi?p={slug}")
            birthday = _get_birthday(page)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Could not find a birth date for '{name}'. Check the spelling.")
    data = clean_career_js(js, birthday)
    data.attrs["player"] = " ".join(re.findall(r"[A-Z][a-z]*", slug)) or name.title()
    return data
