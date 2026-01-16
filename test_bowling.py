import pytest
from bowling_calculator import Bowling

@pytest.fixture
def calc():
    return Bowling()

@pytest.mark.parametrize("rolls, expected", [
    # Example in doc
    (["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"], 149),
    # Perfect game (12 strikes, 300 points)
    (["X"] * 12, 300),
    # All gutter balls (0 points)
    (["0"] * 20, 0),
    # All spares
    (["5", "/"] * 10 + ["5"], 150),
    # No strikes or spares
    (["4", "4"] * 10, 80),
    # Partial game
    (["9", "0", "X", "7", "2"], 37),
])
def test_standard_game_logic(calc, rolls, expected):
    assert calc.calculate_score(rolls) == expected

def test_tenth_frame_strike_bonus(calc):
    rolls = ["0"] * 18 + ["X", "1", "1"] 
    assert calc.calculate_score(rolls) == 12

def test_tenth_frame_spare_bonus(calc):
    rolls = ["0"] * 18 + ["5", "/", "5"]
    assert calc.calculate_score(rolls) == 15

def test_tenth_frame_open_ends_game(calc):
    rolls = ["0"] * 18 + ["4", "4"]
    assert calc.calculate_score(rolls) == 8

@pytest.mark.parametrize("bad_rolls, match_text", [
    (["/", "5"], "cannot start with a spare"),
    (["5", "A", "X"], "Invalid input"),
    (["0"]*18 + ["X", "X", "X", "5"], "Too many rolls in 10th frame"), 
    (["9", "2", "0", "0"], "exceeds 10 pins"),
    (["4", "4"] * 10 + ["5"], "Extra rolls after game completion")
])
def test_validation_rules(calc, bad_rolls, match_text):
    with pytest.raises(ValueError, match=match_text):
        calc.calculate_score(bad_rolls)

def test_invalid_spare_notation(calc):
    bad_notation = ["7", "3", "5", "2"]
    with pytest.raises(ValueError, match="must be recorded as a spare"):
        calc.calculate_score(bad_notation)

def test_frame_exceeds_ten(calc):
    impossible_frame = ["7", "4", "5", "2"]
    with pytest.raises(ValueError, match="exceeds 10 pins"):
        calc.calculate_score(impossible_frame)
