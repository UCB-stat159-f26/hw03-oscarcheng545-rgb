import pytest

from tennis_career.career import (_extract_matches, _get_birthday,
                                  _player_slug, clean_career_js)


def match(date, result, opponent, age):
    row = [""] * 27
    row[0], row[4], row[11], row[16] = date, result, opponent, age
    return row


def javascript(*rows):
    import json
    return "var morematchmx = " + json.dumps(list(rows)) + ";"


def test_womens_birthdates_and_results():
    js = javascript(match("19951030", "L", "Anne Miller", "19770119"),
                    match("19970804", "W", "Amanda Basica", "19780620"))
    data = clean_career_js(js, "1981-09-26")
    assert list(data.result) == ["Loss", "Win"]
    assert data.iloc[0].player_age == pytest.approx(14.09, abs=0.02)
    assert data.iloc[0].opponent_age == pytest.approx(18.78, abs=0.02)
    assert data.iloc[0].age_difference < 0


def test_mens_opponent_ages():
    js = javascript(match("20010910", "L", "First Rival", "21.3"),
                    match("20010917", "W", "Second Rival", "18.7"))
    data = clean_career_js(js, "1986-06-03")
    assert len(data) == 2
    assert data.iloc[0].opponent_age == pytest.approx(21.3)
    assert data.iloc[1].age_difference == pytest.approx(data.iloc[1].player_age - 18.7)


def test_bad_matches_are_skipped():
    js = javascript(match("20010910", "X", "Bad result", "20"),
                    match("20010910", "W", "Missing age", ""),
                    match("20010910", "W", "Good match", "22"))
    assert len(clean_career_js(js, "1986-06-03")) == 1


def test_invalid_file_and_no_valid_matches():
    with pytest.raises(ValueError, match="match table"):
        _extract_matches("not match data")
    with pytest.raises(ValueError, match="No matches with valid ages"):
        clean_career_js(javascript(match("20010910", "X", "Player", "22")), "1986-06-03")


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams", "SerenaWilliams"])
def test_player_spelling(name):
    assert _player_slug(name) == "SerenaWilliams"


def test_missing_birthday():
    assert _get_birthday("Age: 40 (03-Jun-1986)").year == 1986
    with pytest.raises(ValueError, match="date of birth"):
        _get_birthday("No age on this profile")
