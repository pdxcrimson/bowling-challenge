import pytest
from bowling_calculator import Bowling

@pytest.fixture
def calc():
    return Bowling()

def test_provided_example_game(calc):
    rolls = ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"]
    expected = [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]
    assert calc.calculate_score(rolls) == expected

def test_perfect_game(calc):
    rolls = ["X"] * 12
    expected = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
    assert calc.calculate_score(rolls) == expected

def test_all_spares(calc):
    # 5/ in frames 1-10 with a 5 bonus
    rolls = ["5", "/"] * 10 + ["5"]
    expected = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150]
    assert calc.calculate_score(rolls) == expected

# No strikes or spares
def test_all_open_frames(calc):
    rolls = ["4", "4"] * 10
    expected = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80]
    assert calc.calculate_score(rolls) == expected

# Test last frames for strike, spare, and no special rolls
@pytest.mark.parametrize("rolls, expected_final", [
    (["0"]*18 + ["X", "1", "1"], 12), 
    (["0"]*18 + ["5", "/", "5"], 15),
    (["0"]*18 + ["4", "4"], 8),
], ids=["strike_2_bonus", "spare_1_bonus", "open_no_bonus"])

def test_tenth_frame_behavior(calc, rolls, expected_final):
    result = calc.calculate_score(rolls)
    assert result[9] == expected_final

@pytest.mark.parametrize("bad_rolls, match_text", [
    (["/", "5"], "cannot start with a spare"),
    (["5", "A", "X"], "Invalid input"),
    (["0"] * 18 + ["X", "X", "X", "5"], "Too many rolls"), 
    (["9", "2", "0", "0"], "exceeds 10 pins"),
    (["4", "4"] * 10 + ["5"], "Extra rolls after game completion")
])
def test_validation_rules(calc, bad_rolls, match_text):
    with pytest.raises(ValueError, match=match_text):
        calc.calculate_score(bad_rolls)

def test_partial_game_returns_none(calc):
    rolls = ["X", "X"] # Only two frames played
    result = calc.calculate_score(rolls)
    # Frame 1: Strike. Next two rolls? Only one exists ("X"). Cannot score yet.
    assert result[0] is None
    assert result[1] is None
    assert len(result) == 10