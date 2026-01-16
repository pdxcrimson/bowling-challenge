class Bowling:
    def calculate_score(self, rolls: list[str]) -> list[int | None]:
        self._validate_input(rolls)
        total_score = 0
        roll_index = 0
        frame_scores = []

        for frame in range(10):
            if roll_index >= len(rolls):
                break
            
            # Logic for 10th frame (special scoring rule)
            if frame == 9:
                if self._threw_strike(rolls[roll_index]) or \
                   self._threw_spare(rolls[roll_index + 1] if roll_index + 1 < len(rolls) else ""):
                    # 10th frame with strike/spare can have exactly 3 rolls
                    if len(rolls) - roll_index > 3:
                        raise ValueError("Too many rolls in 10th frame")
                    
                    frame_total = (self._get_val(rolls, roll_index) + 
                                   self._get_val(rolls, roll_index + 1) + 
                                   self._get_val(rolls, roll_index + 2))
                    total_score += frame_total
                    roll_index = len(rolls) # Consume all remaining
                else:
                    # Open 10th frame
                    frame_total = self._get_frame_sum(rolls, roll_index)
                    if frame_total >= 10:
                        raise ValueError("must be recorded as a spare (/)")
                    total_score += frame_total
                    roll_index += 2
                
                frame_scores.append(total_score)
                continue

            # Strike (Frames 1-9)
            if self._threw_strike(rolls[roll_index]):
                bonus = self._get_strike_bonus(rolls, roll_index)
                if bonus is None: break # Stop scoring here
                total_score += 10 + bonus
                roll_index += 1
            elif self._threw_spare(rolls[roll_index + 1] if roll_index + 1 < len(rolls) else ""):
                bonus = self._get_spare_bonus(rolls, roll_index)
                if bonus is None: break # Stop scoring here
                total_score += 10 + bonus
                roll_index += 2
            # Other rolls (Frames 1-9)
            else:
                frame_total = self._get_frame_sum(rolls, roll_index)
                if frame_total == 10:
                    raise ValueError("must be recorded as a spare (/)")
                if frame_total > 10:
                    raise ValueError("exceeds 10 pins")
                total_score += frame_total
                roll_index += 2
            
            frame_scores.append(total_score)

        # Post-game validation
        if len(frame_scores) == 10 and roll_index < len(rolls):
            raise ValueError("Extra rolls after game completion")

        # Support for partial games: pad with None until 10 values are present
        while len(frame_scores) < 10:
            frame_scores.append(None)
            
        return frame_scores

    def _threw_strike(self, roll: str) -> bool:
        return str(roll).lower() == 'x'

    def _threw_spare(self, roll: str) -> bool: 
        return roll == '/'

    def _get_strike_bonus(self, rolls: list[str], index: int) -> int | None:
        # A strike needs TWO future rolls to be scorable
        if index + 2 >= len(rolls):
            return None
        return self._get_val(rolls, index + 1) + self._get_val(rolls, index + 2)

    def _get_spare_bonus(self, rolls: list[str], index: int) -> int | None:
        # A spare needs ONE future roll to be scorable
        if index + 2 >= len(rolls):
            return None
        return self._get_val(rolls, index + 2)

    def _get_val(self, rolls: list[str], index: int) -> int:
        if index >= len(rolls): return 0
        val = rolls[index]
        if self._threw_strike(val): return 10
        if val == '/': return 10 - int(rolls[index-1])
        return int(val)

    def _get_frame_sum(self, rolls: list[str], index: int) -> int:
        return self._get_val(rolls, index) + self._get_val(rolls, index + 1)

    def _validate_input(self, rolls: list[str]) -> None:
        if not rolls: return
        if rolls[0] == '/': raise ValueError("Game cannot start with a spare.")
        for roll in rolls:
            if str(roll).lower() not in '0123456789/x':
                raise ValueError("Invalid input: Must be an integer, x, or /")