import pytest
from bowling_calculator import Bowling

@pytest.fixture
def calc():
    return Bowling()

SCENARIOS = [
    (
        # Example in doc
        ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"],
        [15, 24, 33, 58, 78, 93, 101, 110, 129, 149],
        "provided_example"
    ),
    (
        # Perfect game (all strikes)
        ["X"] * 12,
        [30, 60, 90, 120, 150, 180, 210, 240, 270, 300],
        "perfect_game"
    ),
    (
        # All spares
        ["5", "/"] * 10 + ["5"],
        [15, 30, 45, 60, 75, 90, 105, 120, 135, 150],
        "all_spares"
    ),
    (
        # No strikes or spares
        ["4", "4"] * 10,
        [8, 16, 24, 32, 40, 48, 56, 64, 72, 80],
        "all_open_frames"
    ),
]

@pytest.mark.parametrize(
    "rolls, expected, name",
    SCENARIOS,
    ids=[case[2] for case in SCENARIOS]
)
def test_cumulative_scoring_scenarios(calc, rolls, expected, name):
    """Verifies cumulative frame scores for various standard game scenarios."""
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