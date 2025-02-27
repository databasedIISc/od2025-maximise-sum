from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def generate_numbers(n):
    """Generates a shuffled sequence of numbers from 1 to 14."""
    sequence = list(range(1, n+1))
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
    boardLength = request.get_json()['boardLength']
    numbers = generate_numbers(boardLength)
    parity = odd_even_strategy(numbers)
    return jsonify({"numbers": numbers, "strategy": parity})

@app.route('/computer-move', methods=['POST'])
def computer_move():
    """Handles the computer's move based on the strategy."""
    data = request.get_json()
    numbers = data['numbers']
    left, right = data['left'], data['right']
    explanation = "bruh"

    if left > right:
        return jsonify({"choice": None})  # No valid moves left

    # If the user plays as Player 1, the computer (Player 2) uses DP strategy
    if data['player'] == 1:
        # If the user plays as Player 1, the computer (Player 2) uses DP strategy
        dp = compute_dp_table(numbers)

        if left == right:
            explanation = "Since there is only one number ("+str(numbers[left])+") left, I must pick it."
            choice = numbers[left]
        elif dp[left+1][right] < dp[left][right-1]:
            explanation = ("Picking the leftmost number leaves you with a maximum remaining score of "
            +str(dp[left+1][right])+" while the righmost one leaves you with "+str(dp[left][right-1])
            +".<br><br>So, I pick the <b>leftmost</b> number ("+str(numbers[left])+").")
            choice = numbers[left]
        elif dp[left+1][right] > dp[left][right-1]:
            explanation = ("Picking the leftmost number leaves you with a maximum remaining score of "
            +str(dp[left+1][right])+" while the righmost one leaves you with "+str(dp[left][right-1])
            +".<br><br>So, I pick the <b>rightmost</b> number ("+str(numbers[right])+").")
            choice = numbers[right]
        else:
            explanation = ("Picking either the leftmost or the rightmost number leaves you with a maximum remaining score of "
            +str(dp[left+1][right])+".<br><br>So, I can pick any one. I pick the <b>leftmost</b> number ("+str(numbers[left])+").")
            choice = numbers[left]
    else:
        # If the user is Player 2, the computer (Player 1) follows the corrected Odd-Even Strategy
        preferred_parity = data['strategy']
        parity = "odd" if preferred_parity == 0 else "even"

        # Pick the leftmost or rightmost number that matches the preferred parity
        if left % 2 == preferred_parity:
            choice = numbers[left]
            explanation = "I pick the <b>leftmost</b> number ("+str(numbers[left])+"), since it is " + parity + "-indexed."
        else:
            explanation = "I pick the <b>rightmost</b> number ("+str(numbers[right])+"), since it is " + parity + "-indexed."
            choice = numbers[right]

    return jsonify({"choice": choice, "explanation": explanation})

if __name__ == '__main__':
    app.run(debug=True)
 
