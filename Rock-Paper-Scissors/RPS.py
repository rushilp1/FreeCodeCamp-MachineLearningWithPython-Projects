# Program to counter a given move
def counter_move(move):
  # Possible moves in Rock Paper Scissors
  possible_moves = ["R", "P", "S"]
  # Return the move which counters the given move (the move to the right)
  return possible_moves[(possible_moves.index(move) + 1) % 3]

# Program to detect the opponent with which one is playing
def detect_opponent(opponent_history=[]):
  # Check the first five moves that the opponent makes 
  #   and return that particular opponent accordingly
  # (fortunately the first five moves are unique for each opponent)
  if opponent_history[:5] == ['R', 'P', 'P', 'S', 'R']:
    return "quincy"
  if opponent_history[:5] == ['P', 'P', 'S', 'S', 'P']:
    return "abbey"
  if opponent_history[:5] == ['P', 'S', 'S', 'P', 'P']:
    return "kris"
  if opponent_history[:5] == ['R', 'R', 'S', 'S', 'P']:
    return "mrugesh"

# Program to strategize against Quincy
def counter_quincy(opponent_history):
  # All possible moves of Quincy
  #   quincys_moves = ['R', 'R', 'P', 'P', 'S']
  quincys_moves = opponent_history[:5]
  # Predict Quincy's moves as per the round
  predicted_move = quincys_moves[len(opponent_history) % len(quincys_moves)]
  # Return the counter move to predicted move of Quincy
  return counter_move(predicted_move)

# Program to update the likelihood matrix as per the previous and current move
def update_matrix(matrix, previous_move, this_move):
  # Possible moves in Rock Paper Scissors
  possible_moves = ["R", "P", "S"]
  # Get the index of the previous move
  previous_move_index = possible_moves.index(previous_move)
  # Get the index of the current move
  this_move_index = possible_moves.index(this_move)
  # Increase the chances of [previous_move -> this move] event
  matrix[previous_move_index][this_move_index] += 1
  # Return the updated matrix
  return matrix

# Program to get the most likely (next) move as per the given move
def get_most_likely_move(matrix, this_move):
  # Possible moves in Rock Paper Scissors
  possible_moves = ["R", "P", "S"]
  # Get the chances of all transitions from given move
  move_chances = matrix[possible_moves.index(this_move)]
  # Find the most likely move based on one's chances
  most_likely_move_index = move_chances.index(max(move_chances))
  # Get the most likely move based on one's chances
  most_likely_move = possible_moves[most_likely_move_index]
  # Return the most likely move
  return most_likely_move

# Program to strategize against Abbey
def counter_abbey(my_history, opponent_history):
  # Likelihood Matrix (contains occurences of [move1 -> move2] events)
  matrix = [# R2 P2 S2
              [0, 0, 0],  # R1
              [0, 0, 0],  # P1
              [0, 0, 0]   # S1   
            ]
  # Update the Likelihood Matrix for previous moves
  for idx in range(1, len(my_history)):
    matrix = update_matrix(matrix, my_history[idx-1], my_history[idx])
  # Update the Likelihood Matrix for succeeding moves
  for idx in range(5, len(opponent_history)):
    # Predict Abbey's move for that round
    predicted_move = counter_move(get_most_likely_move(matrix, my_history[-1]))
    # Update one's history with the counter move
    my_history.append(counter_move(predicted_move))
    # Update one's next move chances in the matrix
    matrix = update_matrix(matrix, my_history[idx-1], my_history[idx])
  # Predict Abbey's move for that round
  predicted_move = counter_move(get_most_likely_move(matrix, my_history[-1]))
  # Update one's history with the counter move
  my_history.append(counter_move(predicted_move))
  # Return last element of one's history (which contains move for this round)
  return my_history[-1]

# Program to strategize against Kris
def counter_kris(my_history, opponent_history):
  # Traverse through Kris's history...
  for move in opponent_history[5:]:
    # ...and append the corresponding counter move to one's history
    my_history.append(counter_move(move))
  # Predict Kris's move for that round
  predicted_move = counter_move(my_history[-1])
  # Return the counter move to predicted move of Kris
  return counter_move(predicted_move) 

# Program to strategize against Mrugesh
def counter_mrugesh(my_history, opponent_history):
  # Traverse through Mrugesh's history...
  for idx in range(len(opponent_history[5:])):
    # ...get the last ten moves of Mrugesh...
    last_ten = my_history[-10:]
    # ...get Mrugesh's predicted move for that round
    predicted_move = counter_move(max(set(last_ten), key=last_ten.count))
    # ...and append the corresponding counter move to one's history
    my_history.append(counter_move(predicted_move))
  # Return last element of one's history (which contains move for this round)
  return my_history[-1]

# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
def player(prev_play, opponent_history=[]):
  # Append opponent's history in the list
  opponent_history.append(prev_play)

  # Same initial moves for every opponent (useful in determining the opponent)
  my_history = ['', 'P', 'P', 'R', 'R', 'S']
  ## Since every opponent's history is appended in the same list,
  ##   we need to separate every opponent's history for correct detection
  # The maximum length of an opponent's history
  opponent_max_len = 1000
  # The player number (tells us which player is playing)
  player_num = int((len(opponent_history) - 1) / opponent_max_len)
  # Separate the history as per the player number
  new_opponent_history = opponent_history[(1000*player_num):(1000*(player_num+1))]
  
  # If the (current) opponent has played less than 5 moves
  if len(new_opponent_history) <= 5:
    # Play the predefined moves
    return my_history[len(new_opponent_history)]
  else:
    # Else, detect which opponent is playing against us
    opponent = detect_opponent(new_opponent_history[1:])
    # Counter strategize against the detected opponent
    if opponent == "quincy":
      return counter_quincy(new_opponent_history[1:])
    if opponent == "abbey":
      # Remove all 'null' moves from opponent_history
      opponent_history = list(filter(lambda alph: alph != '', opponent_history))
      return counter_abbey(my_history[1:], opponent_history)
    if opponent == "kris":
      return counter_kris(my_history[1:], new_opponent_history[1:])
    if opponent == "mrugesh":
      return counter_mrugesh(my_history[1:], new_opponent_history[1:])