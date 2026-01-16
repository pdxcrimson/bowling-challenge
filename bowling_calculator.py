import pytest

class Bowling:
    def calculate_score(self, rolls: list[str]) -> int:
        self._validate_input(rolls)
        total_score = 0
        roll_index = 0
        frames_played = 0

        for frame in range(10):
            if roll_index >= len(rolls):
                break
            
            frames_played += 1
            
            # Validation for 10th frame roll counts
            if frame == 9:
                is_strike = self._threw_strike(rolls[roll_index])
                is_spare = False
                if not is_strike and roll_index + 1 < len(rolls):
                    is_spare = self._threw_spare(rolls[roll_index + 1])
                
                if (is_strike or is_spare) and len(rolls) - roll_index > 3:
                    raise ValueError("Too many rolls in 10th frame")
            # Strike
            if self._threw_strike(rolls[roll_index]):
                total_score += 10 + self._get_strike_bonus(rolls, roll_index)
                if frame == 9:
                    roll_index = len(rolls)
                else:
                    roll_index += 1

            # Spare
            elif self._threw_spare(rolls[roll_index + 1] if roll_index + 1 < len(rolls) else ""):
                total_score += 10 + self._get_spare_bonus(rolls, roll_index)
                if frame == 9:
                    roll_index = len(rolls)
                else:
                    roll_index += 2
            # Other rolls
            else:
                frame_total = self._get_frame_sum(rolls, roll_index)
                
                if frame_total == 10:
                    raise ValueError(f"Invalid notation: [{rolls[roll_index]}, {rolls[roll_index+1]}] sums to 10 and must be recorded as a spare (/).")
                if frame_total > 10:
                    raise ValueError(f"Invalid frame total: {frame_total} exceeds 10 pins.")

                total_score += frame_total
                roll_index += 2

        if frames_played == 10 and roll_index < len(rolls):
            raise ValueError("Extra rolls after game completion")
            
        return total_score

    def _threw_strike(self, roll: str) -> bool:
        return str(roll).lower() == 'x'

    def _threw_spare(self, roll: str) -> bool: 
        return roll == '/'

    def _get_strike_bonus(self, rolls: list[str], index: int) -> int:
        return self._get_val(rolls, index + 1) + self._get_val(rolls, index + 2)

    def _get_spare_bonus(self, rolls: list[str], index: int) -> int:
        return self._get_val(rolls, index + 2)

    def _get_val(self, rolls: list[str], index: int) -> int:
        if index >= len(rolls): 
            return 0
        val = rolls[index]
        if self._threw_strike(val): 
            return 10
        if val == '/': 
            return 10 - int(rolls[index-1])
        return int(val)

    def _get_frame_sum(self, rolls: list[str], index: int) -> int:
        return self._get_val(rolls, index) + self._get_val(rolls, index + 1)

    def _validate_input(self, rolls: list[str]) -> None:
        if not rolls: 
            return
        if rolls[0] == '/':
            raise ValueError("Game cannot start with a spare.")
        for roll in rolls:
            if str(roll).lower() not in '0123456789/x':
                raise ValueError("Invalid input: Must be an integer, x, or /")

# --- TESTS ---

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

@pytest.mark.parametrize("bad_rolls, match_text", [
    (["/", "5"], "cannot start with a spare"),
    (["5", "A", "X"], "Invalid input"),
    (["0"] * 18 + ["X", "X", "X", "5"], "Too many rolls in 10th frame"), 
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