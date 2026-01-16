# Bowling Challenge Score Calculator

A Python implementation of a 10-Pin Bowling score calculator. This project handles bowling data represented as a stream of roll strings (integers, 'X' for strikes, and '/' for spares).

## Getting Started

### Prerequisites
* **Python 3.10+**

### Environment Setup
Before installing dependencies, it is recommended to use a virtual environment to keep your global Python installation clean.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pdxcrimson/bowling-challenge.git
   cd bowling-challenge
   ```
2. (Optional, but recommended) **Create and activate a virtual environment:**
   - **Linux/MacOS**: 
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

   - **Windows**:
   ```python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependency**:
   
   `pip install pytest`
4. **Running Tests**
   
   `pytest` or `pytest ./test_bowling.py`
   
   **Run with high verbosity (shows individual test IDs):**
   
   `pytest -v` or `pytest ./test_bowling.py -v`

### Design choices ###

1. **Flat list usage** (Option B)
   The calculator follows Option B from the requirements, treating the input as a continuous stream of strings (`list[str]`).
* **Implementation**: The logic uses a `roll_index` pointer. When a strike or spare is encountered, the algorithm "looks ahead" into future indices to calculate bonuses without mutating the original input.
2. **Cumulative output & partial games**
   The calculator returns a list of 10 values representing the cumulative score at the end of each frame.
   * **Partial games**: If a game is incomplete and a frame cannot yet be scored (e.g., a strike is rolled, but the two required bonus rolls haven't happened yet), that frame and all subsequent frames return `None`.
3. **Validation**
   Input checking is used in case of invalid cases. `ValueError` is raised in the following situations:
   * **Valid strings**: Ensures that only `0-9`, `X/x`, and `/` are valid.
   * **Checking for constraints**: Blocking frames that exceed 10 pins (e.g., `["7", "4"]`).
   * **Boundary testing**: Validating the 10th frame specifically for bonus roll eligibility (strikes, spares), and blocking extra rolls after game completion.
4. **Parametrized Testing**
   The test suite uses `@pytest.mark.parametrize` for code reduction, which involves passing parameters with different input and output, including list comprehension in parts. This makes it easier for maintainability.
5. **File breakdown**
   Two `.py` files are used for this to break up code. `bowling_calculator.py` is used to implement the logic for scoring, while `test_bowling.py` is used to run the tests with different types of parameters. This includes both positive and negative testing.
6. **Other**
   Multiple positive and negative test scenarios are used. For positive scenarios, this includes a perfect game, all spares, no spares or strikes, an incomplete game, and all situations in the tenth frame. For negative, this includes starting with a spare, invalid input, exceeding 10 pins, extra rolls, a frame that adds up to 10 points without a spare, and a partial game with only 2 strikes.
