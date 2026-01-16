import pytest

class Bowling:
    def calculate_score(self, rolls: list[str]) -> int:
        self._validate_input(rolls)
        total_score = 0
        roll_index = 0

        for frame in range(10):
            if roll_index >= len(rolls):
                break
            
            # Logic for Strike
            if self._threw_strike(rolls[roll_index]):
                total_score += 10 + self._get_strike_bonus(rolls, roll_index)
                roll_index += 1
            # Logic for Spare
            elif self._threw_spare(rolls[roll_index + 1] if roll_index + 1 < len(rolls) else ""):
                total_score += 10 + self._get_spare_bonus(rolls, roll_index)
                roll_index += 2
            # Logic for Open Frame
            else:
                total_score += self._get_frame_sum(rolls, roll_index)
                roll_index += 2
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
            if roll.lower() not in '0123456789/x':
                raise ValueError("Invalid input: Must be an integer, x, or /")
        # TODO: Handle cases for e.g. [8, 2] when only [8, /] should be correct
@pytest.fixture
def calc():
    return Bowling()
@pytest.mark.parametrize("rolls, expected", [
    (["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"], 149), # Example in doc
    (["X"] * 12, 300),                      # Perfect Game
    (["0"] * 20, 0),                        # Gutter Game
    (["5", "/"] * 10 + ["5"], 150),         # All spares
    (["9", "0", "X", "7", "2"], 37),        # Partial Game
])
def test_valid_scores(calc, rolls, expected):
    assert calc.calculate_score(rolls) == expected

def test_spare_start(calc): 
    with pytest.raises(ValueError, match="Cannot start with a spare"):
        calc.calculate_score(["/", "5", "1"])