import random

def Optimal_Strategy(list_of_numbers):
    """
    num_matrix[i][j] represents the maximum score difference a player can achieve if they play optimally
    on the subarray arr[i...j].
    """
    length_of_list = len(list_of_numbers)
    num_matrix = [[0] * length_of_list for _ in range(length_of_list)]  # Initialize a matrix with zeros
    
    # Base case: When there's only one number in the subarray
    for i in range(length_of_list):
        num_matrix[i][i] = list_of_numbers[i] # Sets the diagonal values to the numbers in the matrix to value at that index
    
    # Fill the matrix for all subarray lengths
    for length in range(2, length_of_list + 1):  # Subarray lengths from 2 to n
        for i in range(length_of_list - length + 1):
            j = i + length - 1  # End of subarray
            # Choose left or right and minimize opponent's score
            num_matrix[i][j] = max(list_of_numbers[i] - num_matrix[i + 1][j], list_of_numbers[j] - num_matrix[i][j - 1])
    
    return num_matrix


def Player_1_Strategy(list_of_numbers, left, right):
    """
    Implements Player 1's odd-even strategy.
    Player 1 calculates the sum of numbers at even indices and odd indices in the current subarray.
    They then prioritize picking numbers from the group (even or odd) with the greater sum.
    """
    # Calculate sums of even-indexed and odd-indexed numbers in the current subarray
    even_sum = sum(list_of_numbers[i] for i in range(left, right + 1, 2))
    odd_sum = sum(list_of_numbers[i] for i in range(left + 1, right + 1, 2))
    
    # Determine which group has greater sum
    if even_sum >= odd_sum:
        target_indices = set(range(left, right + 1, 2))  # Even indices
    else:
        target_indices = set(range(left + 1, right + 1, 2))  # Odd indices
    
    # Choose the number from group (higher sum) that is closest to either end of the array
    if left in target_indices:
        return list_of_numbers[left]
    elif right in target_indices:
        return list_of_numbers[right]
    else:
        # If neither end number is in the target group, choose the end number which is greater
        # This case even though theoretically not possible, has been added due to trust issues
        return list_of_numbers[left] if list_of_numbers[left] >= list_of_numbers[right] else list_of_numbers[right]
    

def Player_2_Strategy(list_of_numbers, matrix, left, right):
    """
    Implements Player 2's optimal strategy using the precomputed matrix.
    Player 2 chooses between the leftmost or rightmost number based on which maximizes their score difference.
    """
    if left == right:
        return list_of_numbers[left]  # If there's only one number left, take it
    
    # Use the matrix to decide whether to pick from the left or right
    if list_of_numbers[left] - matrix[left + 1][right] >= list_of_numbers[right] - matrix[left][right - 1]:
        return list_of_numbers[left]
    else:
        return list_of_numbers[right]


def play_game():
    """
    Allows a user to choose whether they want to be Player 1 or Player 2.
    Computer implements strategy on basis of the player chosen.

    The matrix strategy works for both players, but its easier for player 1 to implement the odd-even strategy and hence easier to explain.
    """
    
    '''
    # Get the initial array of numbers from the user
    numbers = input("Enter the numbers separated by spaces: ").split()
    list_of_numbers = [int(num) for num in numbers]
    '''

    # Generate a random sequence of numbers
    list_of_numbers = random_num_sequence_gen(14)
    
    # Ask which player the user wants to be (Player 1 or Player 2)
    player = int(input("Do you want to be Player 1 or Player 2? Enter 1 or 2: "))
    
    if player not in [1, 2]:
        print("Invalid input. Please enter either '1' or '2'.")
        return
    
    print("List of numbers: ", list_of_numbers) 
       
    # Precompute matrix for computer's strategy if the user chooses to be Player 1
    if player == 1:
        matrix = Optimal_Strategy(list_of_numbers)
    
    # Initialize pointers to track the current subarray (left and right bounds)
    left, right = 0, len(list_of_numbers) - 1
    
    # Initialize scores for player and computer
    player_scores = {1: 0, 2: 0}
    
    # Start with Player 1's turn (current_player = 1)
    current_player = 1
    
    while left <= right:
        if current_player == player:
            # It's the user's turn
            print(f"\nCurrent array: {list_of_numbers[left:right+1]}")  # Show remaining array
            choice = input("Enter 'left' or 'right' to choose a number: ").lower()
            
            if choice == 'left':
                chosen = list_of_numbers[left]
                left += 1
            elif choice == 'right':
                chosen = list_of_numbers[right]
                right -= 1
            else:
                print("Invalid choice. Please enter 'left' or 'right'. \n\n")
                continue
        else:
            # It's the computer's turn
            if current_player == 1:
                chosen = Player_1_Strategy(list_of_numbers, left, right)  # Parity-based strategy for Player 1
            else:
                chosen = Player_2_Strategy(list_of_numbers, matrix, left, right)  # DP-based strategy for Player 2
            
            if chosen == list_of_numbers[left]:
                left += 1
            else:
                right -= 1

        print(f"\nPlayer {current_player} chose: {chosen} \n")
                    
        # Update scores after each turn
        player_scores[current_player] += chosen
        print(f"Player {current_player} score: {player_scores[current_player]}")
        
        # Switch turns between player and computer
        current_player = 3 - current_player
    
    print("\nGame Over!")
    
    # Display final scores and determine winner

    if player == 1:
        print("Your (Player 1) final score: ", player_scores[1])
        print("Computer (Player 2) final score: ", player_scores[2])
    else:
        print("Your (Player 2) final score: ", player_scores[2])
        print("Computer (Player 1) final score: ", player_scores[1])
    
    if player_scores[1] > player_scores[2]:
        print("Player 1 wins!")
    elif player_scores[2] > player_scores[1]:
        print("Player 2 wins!")
    else:
        print("It's a tie!")


def random_num_sequence_gen(size):
    """
    Generates a random sequence of numbers from 1 to size (both included).
    """
    sequence = list(range(1, size + 1))
    random.shuffle(sequence)
    return sequence

play_game()
