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