from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def generate_numbers():
    """Generates 14 random numbers between 1 and 99 (inclusive) with an odd sum."""
    while True:
        sequence = [random.randint(1, 99) for _ in range(14)]
        if sum(sequence) % 2 == 1:
            random.shuffle(sequence)
            return sequence


def compute_dp_table(numbers):
    """Computes the DP table for the optimal strategy when the computer is Player 2."""
    n = len(numbers)
    dp = [[0] * n for _ in range(n)]

    # Base case: When there's only one element, take it
    for i in range(n):
        dp[i][i] = numbers[i]

    # Fill DP table for subarrays of length 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            pick_left = numbers[i] + min(dp[i+2][j] if i+2 <= j else 0, dp[i+1][j-1] if i+1 <= j-1 else 0)
            pick_right = numbers[j] + min(dp[i+1][j-1] if i+1 <= j-1 else 0, dp[i][j-2] if i <= j-2 else 0)
            dp[i][j] = max(pick_left, pick_right)

    return dp

def odd_even_strategy(numbers):
    """Determines whether the sum of odd or even indexed numbers is greater."""
    odd_sum = sum(numbers[i] for i in range(0, len(numbers), 2))
    even_sum = sum(numbers[i] for i in range(1, len(numbers), 2))

    preferred_parity = 0 if odd_sum > even_sum else 1  # 0 → Pick from odd indices, 1 → Pick from even indices
    return preferred_parity

@app.route('/')
def home():
    """Renders the main game page."""
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    """Starts a new game and sends the generated numbers to the frontend."""
    numbers = generate_numbers()
    return jsonify({"numbers": numbers})

@app.route('/computer-move', methods=['POST'])
def computer_move():
    """Handles the computer's move based on the strategy."""
    data = request.get_json()
    numbers = data['numbers']
    left, right = 0, len(numbers) - 1

    if left > right:
        return jsonify({"choice": None})  # No valid moves left

    if data['player'] == 1:
        # If the user plays as Player 1, the computer (Player 2) uses DP strategy
        dp = compute_dp_table(numbers)
        if dp[left+1][right] if left+1 <= right else 0 <= dp[left][right-1] if left <= right-1 else 0:
            choice = numbers[right]
        else:
            choice = numbers[left]
    else:
        # If the user is Player 2, the computer (Player 1) follows the corrected Odd-Even Strategy
        preferred_parity = odd_even_strategy(numbers)

        # Pick the leftmost or rightmost number that matches the preferred parity
        if left % 2 == preferred_parity:
            choice = numbers[left]
        else:
            choice = numbers[right]

    return jsonify({"choice": choice})

if __name__ == '__main__':
    app.run(debug=True)
 
